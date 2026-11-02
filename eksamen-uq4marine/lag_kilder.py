# /// script
# requires-python = ">=3.10"
# dependencies = ["pypdf>=5,<7"]
# ///
"""Lag lesbare tekstkilder til NotebookLM, Gemini, Perplexity og Copilot.

NotebookLM og Gemini leser ikke .py-filer godt, og Copilot leser ikke PDF-er.
Dette skriptet gjør alt om til Markdown (.md).

Bruk (fra mappen eksamen-uq4marine):
    uv run lag_kilder.py

Resultat i kilder/ (lages på nytt hver gang, så ikke legg egne filer der):
    skript/     ett .md per kursskript (forklaring + kodeblokker)
    pdf/        tekst fra PDF-er i materiale/ og kurs/documents/
    dokumenter/ kursets egne .md-guider og modellnotater
    kurs_README.md
    _samlet_kurs.md   alt i én fil, til verktøy med få filplasser (f.eks. en Gemini-Gem)
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROT = Path(__file__).resolve().parent
KURS = ROT / "kurs"
MATERIALE = ROT / "materiale"
UT = ROT / "kilder"


def skript_til_md(sti: Path) -> str:
    """Gjør en fil med '# %%'-celler om til Markdown."""
    ut = [f"Kilde: kurs/{sti.relative_to(KURS).as_posix()}", ""]
    modus = "kode"
    kode: list[str] = []

    def lukk_kode() -> None:
        while kode and not kode[0].strip():
            kode.pop(0)
        while kode and not kode[-1].strip():
            kode.pop()
        if kode:
            ut.extend(["```python", *kode, "```", ""])
        kode.clear()

    for linje in sti.read_text(encoding="utf-8").splitlines():
        s = linje.strip()
        if s.startswith("# %% [markdown]"):
            lukk_kode()
            modus = "md"
        elif s.startswith("# %%"):
            lukk_kode()
            modus = "kode"
        elif modus == "md":
            ut.append(s[2:] if s.startswith("# ") else s.lstrip("#"))
        else:
            kode.append(linje.rstrip())
    lukk_kode()
    return "\n".join(ut).strip() + "\n"


def pdf_til_md(pdf: Path) -> str:
    from pypdf import PdfReader

    leser = PdfReader(pdf)
    deler = [f"Kilde: {pdf.relative_to(ROT).as_posix()}", ""]
    for nr, side in enumerate(leser.pages, 1):
        tekst = (side.extract_text() or "").strip()
        deler += [f"## Side {nr}", "", tekst or "(ingen tekst – trolig skannet bilde)", ""]
    return "\n".join(deler)


def flatt_navn(sti: Path) -> str:
    """materiale/uke 1/slides.pdf -> materiale__uke 1__slides.md (unikt navn)."""
    return "__".join(sti.relative_to(ROT).with_suffix(".md").parts)


def ord_i(tekst: str) -> int:
    return len(tekst.split())


def main() -> None:
    # Slett bare det dette skriptet lager selv – ikke notebooklm/ og notebooks/ fra lag_notebooklm.py.
    for mappe in ("skript", "pdf", "dokumenter"):
        shutil.rmtree(UT / mappe, ignore_errors=True)
        (UT / mappe).mkdir(parents=True)
    for fil in ("kurs_README.md", "_samlet_kurs.md"):
        (UT / fil).unlink(missing_ok=True)

    laget: list[tuple[Path, str]] = []

    def skriv(sti: Path, tekst: str) -> None:
        sti.write_text(tekst, encoding="utf-8")
        laget.append((sti, tekst))

    if KURS.is_dir():
        readme = KURS / "README.md"
        if readme.exists():
            skriv(UT / "kurs_README.md", f"Kilde: kurs/README.md\n\n{readme.read_text(encoding='utf-8')}")
        for py in sorted((KURS / "pyscripts").glob("*.py")):
            skriv(UT / "skript" / f"{py.stem}.md", skript_til_md(py))
        for md in sorted((KURS / "documents").rglob("*.md")):
            skriv(UT / "dokumenter" / flatt_navn(md), f"Kilde: {md.relative_to(ROT).as_posix()}\n\n{md.read_text(encoding='utf-8')}")
    else:
        print("⚠️  Fant ikke kurs/ – kjør  bash oppsett.sh  først. Fortsetter med materiale/.")

    pdfer = sorted(MATERIALE.rglob("*.pdf")) + sorted((KURS / "documents").rglob("*.pdf"))
    for pdf in pdfer:
        try:
            skriv(UT / "pdf" / flatt_navn(pdf), pdf_til_md(pdf))
        except Exception as feil:  # kryptert eller ødelagt PDF – hopp over, ikke stopp alt
            print(f"⚠️  Hoppet over {pdf.relative_to(ROT)}: {feil}")

    samlet = "\n\n---\n\n".join(f"# FIL: {sti.relative_to(UT).as_posix()}\n\n{tekst}" for sti, tekst in laget)
    (UT / "_samlet_kurs.md").write_text(samlet, encoding="utf-8")

    for sti, tekst in laget:
        print(f"  ✅ {sti.relative_to(ROT).as_posix():60s} {ord_i(tekst):>7,} ord")
    print(f"\n  📦 kilder/_samlet_kurs.md: {ord_i(samlet):,} ord totalt ({len(laget)} filer)")
    print("  Neste: last opp kilder/skript, kilder/pdf og kilder/dokumenter til NotebookLM.")


if __name__ == "__main__":
    main()
