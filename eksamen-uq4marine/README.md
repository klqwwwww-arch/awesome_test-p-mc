# Eksamen UQ4Marine: studieoppsett

VS Code, Copilot, NotebookLM, Gemini, Perplexity og Notion koblet sammen for emnet
*Numerical Methods in Uncertainty Quantification of Marine Applications*.
Kursfiler: https://github.com/Hugo-build/numerical_uq4marine_course

> ⚠️ **Først:** repoet denne mappen ligger i nå (`awesome_test-p-mc`) er **offentlig**.
> Ikke last opp kursmateriale hit. Flytt oppsettet til et **privat** repo på den nye kontoen (steg 1).

## Start (3 steg)

1. **Ny GitHub-konto + privat repo:** [guider/1-github-ny-konto.md](guider/1-github-ny-konto.md)
2. **Installer og sjekk alt med én kommando:**
   ```sh
   bash oppsett.sh
   ```
   Skriptet sjekker Git, installerer uv, henter kurset til `kurs/`, lager Python-miljøet, kjører leksjon 01 som test og installerer VS Code-utvidelsene. Det er trygt å kjøre på nytt, og en ny kjøring oppdaterer kurset.
3. **Åpne og kjør:**
   ```sh
   code .
   ```
   Åpne `kurs/pyscripts/01_vectors_matrices.py` → **Run Cell**. Copilot-oppsett: [guider/2-vscode-copilot.md](guider/2-vscode-copilot.md)

Etterpå: legg PDF-er i `materiale/`, kjør `uv run lag_kilder.py` og last opp `kilder/` til NotebookLM og Gemini.
Se [guider/3-ai-verktoy.md](guider/3-ai-verktoy.md).

## Mappene

```text
eksamen-uq4marine/
├── oppsett.sh               ← kjør først (og når kurset er oppdatert)
├── lag_kilder.py            ← PDF + kursskript → .md for KI-verktøy
├── pensum.md                ← temaer, fremdrift, eksamensspørsmål
├── guider/                  ← 1 GitHub · 2 VS Code/Copilot · 3 KI-verktøy
├── notater/                 ← dine oppsummeringsark (_mal.md)
├── ovinger/                 ← dine kopier av skript og løsninger
├── materiale/               ← dine PDF-er (lastes ikke opp til GitHub)
├── kurs/                    ← forelesers repo, ikke endre (lages av oppsett.sh)
├── kilder/                  ← genererte tekstfiler (lages av lag_kilder.py)
├── .github/copilot-instructions.md + prompts/   ← Copilot: norsk, hint før fasit, /forklar /oving …
└── .vscode/                 ← Python-tolk = kurs/.venv, anbefalte utvidelser
```

## Hverdagen

| Økt | Hva |
|---|---|
| **Vanlig (45 min)** | Velg tema i `pensum.md`/Notion → kjør skriptet → `/forklar` → endre én parameter → quiz i NotebookLM → oppdater status |
| **Lett dag (15 min)** | `/lett-dag` i Copilot *eller* en lydoversikt i NotebookLM |
| **Lagre** | `git add . && git commit -m "notater" && git push` |

## Hva er forbedret fra datalab-e-posten
- **Ett skript** i stedet for 7 manuelle steg. Det stopper med en tydelig melding hvis noe mangler.
- `uv sync --locked`: samme pakkeversjoner som foreleser (står i kursets README).
- **Mac:** Git krever `xcode-select --install`, og `code .` krever «Shell Command: Install 'code' command in PATH». Skriptet sier fra om begge.
- **Sikkerhet:** `curl … | sh` kjøres bare etter at du har sagt ja. Homebrew brukes hvis du har det.
- **Kurset ligger i `kurs/`, dine filer ved siden av.** Kursoppdateringer krasjer ikke med notatene dine.
- **Røyktest:** leksjon 01 kjøres automatisk, så du vet at alt virker før timen.
