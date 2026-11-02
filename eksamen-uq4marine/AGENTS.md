# AGENTS.md · instruks for Codex og andre kodeagenter

Studieoppsett for eksamensforberedelse (UiS, marin/offshore). Eieren vil ha det **enkelt, trygt og lett på disk**.
Han har dager med lite energi: små, tydelige endringer som er lette å se over.

## Regler (alltid)

- Norsk i tekst, kommentarer og meldinger. Engelske fagbegreper er greit.
- **Én oppgave = én branch = én PR.** Hold diffen liten (helst under 150 linjer). Spar tokens: ikke skriv om filer som virker.
- **Ikke endre `kurs/`** (forelesers repo). Ikke commit `kilder/`, `materiale/`, `logs/`, `.venv/`.
- **Ingen hemmeligheter eller persondata** i kode, logger, tester eller commits: ingen tokens, e-post, studentnummer, helseinfo.
- **Ingen nye avhengigheter** uten å spørre. Bruk standardbiblioteket + det kurset har (numpy, scipy, matplotlib, pypdf).
- **Ingen nye nettverkskall.** `curl … | sh` bare etter ja fra brukeren (slik `oppsett.sh` gjør nå).
- Ikke slett filer, endre git-historikk eller kjør `rm -rf` uten å spørre.
- Kjør sjekkene under før PR, og vis resultatet i PR-beskrivelsen.

## Sjekker før PR

```sh
bash -n oppsett.sh && shellcheck oppsett.sh   # shellcheck: brew install shellcheck
python3 -m py_compile lag_kilder.py lag_notebooklm.py
python3 -m unittest discover -s tests          # når tests/ finnes
kurs/.venv/bin/python lag_notebooklm.py 01     # røyktest: lager kilder/notebooklm/01_*.pdf
```

## Oppgaver (én om gangen, i denne rekkefølgen)

### 1 · Sikkerhet
- Fiks alle shellcheck-funn i `oppsett.sh`.
- Før `git pull` i `kurs/`: sjekk at `origin` faktisk er `KURS_URL`. Stopp med tydelig melding hvis ikke.
- `.gitignore`: legg til `logs/` og `*.log`.
- Valgfri pre-commit-hook i `verktoy/pre-commit` (installeres med én kommando i README) som stopper filer over 5 MB og mønstre som `ghp_`, `sk-`, `AKIA`, `-----BEGIN`.

### 2 · Feillogging
- Logg til `logs/` med Pythons `logging` + `RotatingFileHandler` (1 MB × 3 filer).
- Logg tidspunkt, steg, varighet og feil med traceback. **Aldri** miljøvariabler eller filinnhold.
- `oppsett.sh`: skriv også til `logs/oppsett.log` (`tee -a`), og `trap … ERR` som logger linjenummer og kommando.
- Ved feil: én kort linje i terminalen + «se logs/…». Avslutt med exit-kode ≠ 0.

### 3 · Robusthet
- `lag_notebooklm.py`: `--timeout` per skript (standard 1800 s) og exit-kode ≠ 0 hvis noe feilet.
- `--sjekk` i begge Python-skriptene: viser hva som mangler (git, uv, pandoc, xelatex, ledig disk) uten å endre noe.
- Tester i `tests/` med `unittest` (standardbiblioteket): `les_celler`, `pensum_kjerne`, `bryt`, og at `lag_kilder.py` ikke sletter `kilder/notebooklm/`.

### 4 · Lett på disk
- `bash oppsett.sh --lett`: installer bare numpy, scipy og matplotlib i `kurs/.venv` (ikke JupyterLab), hopp over VS Code-utvidelser.
- `bash rydd.sh`: vis størrelsen på `kilder/`, `kurs/.venv` og uv-cachen, og slett bare det brukeren svarer ja til. Avslutt med `uv cache prune`.

### 5 · Nytt fag (gjenbruk av oppsettet)
- `bash nytt-fag.sh KODE "Emnenavn" [kurs-repo-url]` lager `../eksamen-<kode>/` fra denne mappen:
  guider, prompts, `.vscode/`, `.gitignore`, skriptene, `AGENTS.md`, og en tom `pensum.md` med samme tabellformat.
- Bytt emnenavn i `README.md` og `.github/copilot-instructions.md`. Ikke kopier `kurs/`, `kilder/`, `materiale/` eller notater.
- Uten kurs-repo: hopp over kloning. Da brukes bare Canvas-PDF-er i `materiale/` → `lag_kilder.py`.
- Legg til én linje i README om kommandoen.

## Ferdig når
Sjekkene over er grønne, README har én linje per ny kommando, og PR-en forklarer på 3–5 punkter hva som er endret og hvordan det testes.
