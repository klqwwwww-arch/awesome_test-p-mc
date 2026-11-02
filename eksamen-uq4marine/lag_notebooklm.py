"""Kjør kursskriptene og lag én PDF per tema (tekst, formler, kode, figurer) + kjørte notebooks.

Hvorfor: NotebookLM leser ikke .py-filer, og figurene finnes bare når skriptet kjøres.
Her kjøres hvert skript celle for celle (som i VS Code), figurene lagres, og alt
settes sammen til et lesbart hefte per tema – klart for NotebookLM og repetisjon.

Bruk (fra mappen eksamen-uq4marine, etter  bash oppsett.sh):
    kurs/.venv/bin/python lag_notebooklm.py          # alle skript (ca. 5–15 min)
    kurs/.venv/bin/python lag_notebooklm.py 07 08    # bare noen

Resultat i kilder/ (lages på nytt, ikke legg egne filer der):
    notebooklm/   én PDF per tema + oversikt + artikkel  → last opp til NotebookLM
    notebooks/    .ipynb med figurer og utskrift          → åpne i VS Code
PDF krever pandoc + xelatex. Mangler de, lages .md i stedet (tekst uten figurer i NotebookLM).
"""

from __future__ import annotations

import base64
import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

ROT = Path(__file__).resolve().parent
KURS = ROT / "kurs"
UT = ROT / "kilder"
PDF_UT = UT / "notebooklm"
NB_UT = UT / "notebooks"
MAKS_LINJER = 60  # utskrift per celle i PDF-en


# ---------- deling i celler ----------

def les_celler(sti: Path) -> list[tuple[str, str]]:
    """'# %% [markdown]' og '# %%' → [(type, tekst)]."""
    celler: list[tuple[str, str]] = []
    modus, buf = "kode", []

    def lukk() -> None:
        tekst = "\n".join(buf).strip("\n")
        if tekst.strip():
            celler.append((modus, tekst))
        buf.clear()

    for linje in sti.read_text(encoding="utf-8").splitlines():
        s = linje.strip()
        if s.startswith("# %% [markdown]"):
            lukk()
            modus = "md"
        elif s.startswith("# %%"):
            lukk()
            modus = "kode"
        elif modus == "md":
            s = linje.lstrip()
            buf.append(s[2:] if s.startswith("# ") else s[1:] if s.startswith("#") else s)
        else:
            buf.append(linje.rstrip())
    lukk()
    return celler


# ---------- kjøring (egen prosess per skript) ----------

def arbeider(skript: Path, figurmappe: Path, resultat: Path) -> None:
    os.environ["MPLBACKEND"] = "Agg"
    import warnings

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    warnings.simplefilter("ignore")
    figurmappe.mkdir(parents=True, exist_ok=True)
    figurer: list[str] = []

    def lagre_figurer(*_a, **_k) -> None:
        for nr in plt.get_fignums():
            navn = f"{skript.stem}_fig{len(figurer) + 1:02d}.png"
            plt.figure(nr).savefig(figurmappe / navn, dpi=110, bbox_inches="tight")
            figurer.append(navn)
        plt.close("all")

    plt.show = lagre_figurer  # vis = lagre, som «inline» i Jupyter
    ns = {"__name__": "__main__", "__file__": str(skript)}
    os.chdir(skript.parent)
    ut = []
    for i, (type_, tekst) in enumerate(les_celler(skript)):
        if type_ != "kode":
            ut.append({"type": "md", "tekst": tekst})
            continue
        start = len(figurer)
        buf, feil = io.StringIO(), ""
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            try:
                exec(compile(tekst, f"{skript.name} (celle {i + 1})", "exec"), ns)
            except Exception:
                feil = traceback.format_exc(limit=3)
            finally:
                lagre_figurer()
        ut.append({"type": "kode", "tekst": tekst, "utskrift": buf.getvalue(),
                   "feil": feil, "figurer": figurer[start:]})
    resultat.write_text(json.dumps(ut, ensure_ascii=False), encoding="utf-8")


# ---------- sammenstilling ----------

def pensum_kjerne() -> dict[str, tuple[str, str]]:
    """Leser '| ⬜ | 07 | Tema | Kjerne |' fra pensum.md."""
    fil = ROT / "pensum.md"
    if not fil.exists():
        return {}
    rader = re.findall(r"^\|[^|]*\|\s*([0-9][0-9-]*)\s*\|([^|]+)\|([^|]+)\|", fil.read_text(encoding="utf-8"), re.M)
    return {nr: (tema.strip(), kjerne.strip()) for nr, tema, kjerne in rader}


def bryt(tekst: str) -> str:
    linjer = []
    for linje in tekst.rstrip().splitlines():
        linjer += textwrap.wrap(linje, 100, replace_whitespace=False, drop_whitespace=False) or [""]
    if len(linjer) > MAKS_LINJER:
        linjer = linjer[:MAKS_LINJER] + [f"… ({len(linjer) - MAKS_LINJER} linjer til, se notebooken)"]
    return "\n".join(linjer)


def lag_markdown(skript: Path, celler: list[dict], kjerne: dict) -> str:
    nr = skript.stem.split("_")[0]
    tema = kjerne.get(nr)
    deler = [f"*Kilde: kurs/pyscripts/{skript.name} · Numerical Method in Uncertainty Quantification "
             f"of Marine Applications · kjørt {date.today():%d.%m.%Y}*", ""]
    if tema:
        deler += [f"> **Pensum {nr} – {tema[0]}.** Kjerne: {tema[1]}", ""]
    for c in celler:
        if c["type"] == "md":
            deler += [c["tekst"], ""]
            continue
        deler += ["```python", c["tekst"], "```", ""]
        if c["utskrift"].strip():
            deler += ["**Utskrift:**", "", "```text", bryt(c["utskrift"]), "```", ""]
        if c["feil"]:
            deler += ["**Feil ved kjøring:**", "", "```text", bryt(c["feil"]), "```", ""]
        for fig in c["figurer"]:
            deler += [f"![](figurer/{fig}){{width=92%}}", ""]
    return "\n".join(deler)


def lag_notebook(celler: list[dict], figurmappe: Path) -> dict:
    nb_celler = []
    for n, c in enumerate(celler, 1):
        cid = uuid.uuid4().hex[:8]
        if c["type"] == "md":
            nb_celler.append({"cell_type": "markdown", "id": cid, "metadata": {}, "source": c["tekst"]})
            continue
        utdata = []
        if c["utskrift"]:
            utdata.append({"output_type": "stream", "name": "stdout", "text": c["utskrift"]})
        if c["feil"]:
            utdata.append({"output_type": "stream", "name": "stderr", "text": c["feil"]})
        for fig in c["figurer"]:
            png = base64.b64encode((figurmappe / fig).read_bytes()).decode()
            utdata.append({"output_type": "display_data", "metadata": {},
                           "data": {"image/png": png, "text/plain": "<Figure>"}})
        nb_celler.append({"cell_type": "code", "id": cid, "metadata": {}, "execution_count": n,
                          "source": c["tekst"], "outputs": utdata})
    return {"nbformat": 4, "nbformat_minor": 5, "cells": nb_celler,
            "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                         "language_info": {"name": "python"}}}


PDF_HODE = r"""
\usepackage{fvextra}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,breakanywhere,commandchars=\\\{\}}
\usepackage{etoolbox}
\AtBeginEnvironment{Shaded}{\footnotesize}
\AtBeginEnvironment{verbatim}{\footnotesize}
"""


def lag_pdf(md: Path) -> str:
    """Returnerer '' ved suksess, ellers feilmelding."""
    if not (shutil.which("pandoc") and shutil.which("xelatex")):
        return "pandoc/xelatex mangler"
    hode = md.parent / "_hode.tex"
    hode.write_text(PDF_HODE, encoding="utf-8")
    kmd = ["pandoc", md.name, "-o", md.with_suffix(".pdf").name, "--pdf-engine=xelatex",
           "-f", "markdown-implicit_figures", "-H", hode.name,
           "-V", "geometry:margin=1.8cm", "-V", "papersize=a4", "-V", "fontsize=10pt",
           "-V", "colorlinks=true", "-V", "lang=nb"]
    # DejaVu (Linux) har greske tegn i brødteksten. Mac: prøv macOS-fonter, til slutt standardfontene.
    fontsett = [["mainfont=DejaVu Serif", "sansfont=DejaVu Sans", "monofont=DejaVu Sans Mono", "mathfont=Latin Modern Math"],
                ["mainfont=Times New Roman", "sansfont=Helvetica", "monofont=Menlo", "mathfont=STIX Two Math"],
                []]
    for fonter in fontsett:
        r = subprocess.run(kmd + [a for f in fonter for a in ("-V", f)], cwd=md.parent, capture_output=True, text=True)
        if r.returncode == 0:
            return ""
    return (r.stderr or r.stdout)[-1500:]


def behandle(skript: Path, arbeidsrot: Path) -> tuple[str, str]:
    figurmappe = PDF_UT / "figurer"
    res = arbeidsrot / f"{skript.stem}.json"
    try:
        r = subprocess.run([sys.executable, __file__, "--arbeider", str(arbeidsrot / "pyscripts" / skript.name),
                            str(figurmappe), str(res)], capture_output=True, text=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return skript.stem, "❌ tidsavbrudd (30 min)"
    if r.returncode != 0 or not res.exists():
        return skript.stem, "❌ " + (r.stderr or "ukjent feil")[-800:]
    celler = json.loads(res.read_text(encoding="utf-8"))
    md = PDF_UT / f"{skript.stem}.md"
    md.write_text(lag_markdown(skript, celler, pensum_kjerne()), encoding="utf-8")
    (NB_UT / f"{skript.stem}.ipynb").write_text(
        json.dumps(lag_notebook(celler, figurmappe), ensure_ascii=False, indent=1), encoding="utf-8")
    feil = sum(1 for c in celler if c.get("feil"))
    pdf_feil = lag_pdf(md)
    if not pdf_feil:
        md.unlink()
    figurer = sum(len(c.get("figurer", [])) for c in celler)
    status = f"{'✅' if not feil else '⚠️'} {figurer} figurer" + (f", {feil} celler feilet" if feil else "")
    return skript.stem, status + (f" · PDF feilet: {pdf_feil}" if pdf_feil else "")


def main(valg: list[str]) -> None:
    if not (KURS / "pyscripts").is_dir():
        sys.exit("Fant ikke kurs/pyscripts – kjør  bash oppsett.sh  først.")
    skript = sorted((KURS / "pyscripts").glob("*.py"))
    if valg:
        skript = [s for s in skript if any(s.name.startswith(v) for v in valg)]
    for mappe in (PDF_UT, NB_UT):
        if mappe.exists() and not valg:
            shutil.rmtree(mappe)
        mappe.mkdir(parents=True, exist_ok=True)

    # Kjør i en kopi, så skript som skriver filer (06) ikke roter til kurs/.
    with tempfile.TemporaryDirectory() as tmp:
        arbeidsrot = Path(tmp)
        shutil.copytree(KURS / "pyscripts", arbeidsrot / "pyscripts")
        with ThreadPoolExecutor(max_workers=max(1, min(4, (os.cpu_count() or 2) - 1))) as pool:
            for navn, status in pool.map(lambda s: behandle(s, arbeidsrot), skript):
                print(f"  {navn:42s} {status}", flush=True)
        forhånd = arbeidsrot / "previews"
        if forhånd.exists():
            shutil.copytree(forhånd, UT / "animasjoner", dirs_exist_ok=True)

    # Faste kilder: oversikt, metocean-artikkel og modellnotater
    oversikt = ["# Oversikt: pensum, fremdrift og eksamensspørsmål", ""]
    if (ROT / "pensum.md").exists():
        oversikt.append((ROT / "pensum.md").read_text(encoding="utf-8"))
    if (KURS / "README.md").exists():
        oversikt += ["", "---", "", "# Forelesers README (kurs/README.md)", "",
                     (KURS / "README.md").read_text(encoding="utf-8")]
    (PDF_UT / "00_oversikt_pensum_og_kurs.md").write_text("\n".join(oversikt), encoding="utf-8")
    for fil in (KURS / "documents" / "five_site_models").glob("*"):
        if fil.suffix in {".pdf", ".md"}:
            shutil.copy2(fil, PDF_UT / f"05_kilde_{fil.name}")
    # Figurene ligger inne i PDF-ene. Mappa trengs bare hvis noen PDF-er feilet (.md-reserve).
    if not any((PDF_UT / f"{s.stem}.md").exists() for s in skript):
        shutil.rmtree(PDF_UT / "figurer", ignore_errors=True)
    (PDF_UT / "_hode.tex").unlink(missing_ok=True)
    print(f"\n  📦 Last opp alt i {PDF_UT.relative_to(ROT)}/ til NotebookLM. Notebooks: {NB_UT.relative_to(ROT)}/")


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "--arbeider":
        arbeider(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
    else:
        main(sys.argv[1:])
