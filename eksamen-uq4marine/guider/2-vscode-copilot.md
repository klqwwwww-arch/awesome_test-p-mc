# 2 · VS Code + Copilot

## Koble Copilot til den nye kontoen
1. Åpne mappen: `code ~/Studie/eksamen-uq4marine`
2. Klikk person-ikonet nede til venstre. Er den gamle kontoen innlogget, velg **Sign out** først.
3. **Sign in with GitHub to use GitHub Copilot** → logg inn med den nye kontoen.
4. Sjekk plan og forbruk: https://github.com/settings/copilot
5. Personvern, samme side: slå **av** at GitHub kan bruke dataene dine til produktforbedring.

> **Kvoter:** Copilot har en gratisplan for alle og en studentplan (via GitHub Education). Fra juni 2026 bruker GitHub
> AI-kreditter i stedet for «premium requests», og tallene endres ofte. Derfor står ingen tall her. Se gjeldende kvote
> på https://github.com/settings/copilot og kryssjekk i Perplexity.

## Første gang i VS Code
- Godta «Install recommended extensions» (Python, Jupyter, Copilot Chat). Dette gjør også `bash oppsett.sh`.
- `Cmd+Shift+P` → **Python: Select Interpreter** → `kurs/.venv/bin/python`
- Åpne `kurs/pyscripts/01_vectors_matrices.py` → klikk **Run Cell** over `# %%`. Resultatet vises i et interaktivt vindu.

## Bruk kvoten smart (mest læring per forespørsel)

| Hva | Hvordan | Når |
|---|---|---|
| Fullføringer (grå tekst) | `Tab` for å godta | Når du skriver egne øvinger |
| Inline-chat | Marker kode → `Cmd+I` | «Hva gjør denne linjen?» |
| Chat-panel | `Ctrl+Cmd+I` | Lengre forklaringer, flere filer |
| Ferdige prompter | Skriv `/` i chatten | Se tabellen under |
| Kontekst | `#file:kurs/pyscripts/07_short_term_extremes.py` | Så svaret holder seg til pensum |

Ferdige prompter i `.github/prompts/`:

| Kommando | Gjør |
|---|---|
| `/forklar` | Forklarer åpen fil eller markert kode: formel, kode, tolkning, kontrollspørsmål |
| `/oving` | 3 eksamensliknende oppgaver med hint → `ovinger/` |
| `/sjekk` | Retter løsningen din med hint, ikke fasit |
| `/oppsummer` | Oppsummeringsark på én side → `notater/` |
| `/kort` | 15 flashcards som CSV, for import til Notion |
| `/lett-dag` | Økt på 15 min for dager med lite energi |

Tips:
- **Ask**-modus for spørsmål, **Agent**-modus når Copilot skal lage filer (`/oving`, `/oppsummer`, `/kort`).
- Modellvalg **Auto** holder forbruket nede. Bytt til en sterkere modell bare for tunge utledninger.
- Én tydelig forespørsel med `#file` gir mer enn ti vage.
- Copilot leser instruksene i `.github/copilot-instructions.md` automatisk: norsk, hint før fasit og kursets konvensjoner.
- PDF-er: kjør `uv run lag_kilder.py` og bruk `#file:kilder/pdf/...`, ikke selve PDF-en.
