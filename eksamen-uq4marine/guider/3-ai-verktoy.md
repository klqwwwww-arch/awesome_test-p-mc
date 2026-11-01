# 3 · Perplexity, Gemini, NotebookLM, Notion: hvem gjør hva

Prinsipp: **lag kildene én gang** (`uv run lag_kilder.py`), og bruk dem i alle verktøy.

| Verktøy | Bruk til | Ikke til |
|---|---|---|
| **VS Code + Copilot** | Kjøre og forstå kursskript, øvinger, feilsøking | Fakta om eksamen og frister |
| **NotebookLM** | «Spør pensum»: quiz, flashcards, lydoversikt, svar med kildehenvisning | Kjøre kode |
| **Gemini Pro** | Lange forklaringer, sjekke foto av håndregning | Siste nytt |
| **Perplexity Pro** | Eksterne kilder med lenker: standarder (f.eks. DNV-RP-C205), artikler, definisjoner | Detaljer i pensum (bruk NotebookLM) |
| **Notion** | Plan, fremdrift, feillogg, flashcards | Lange forklaringer |
| **Claude** | Resonnering, sjekke utledninger, skriving | Kjøre kode lokalt |

## NotebookLM (start her, gir mest læring per minutt)
1. https://notebooklm.google.com → **Ny notatbok** «UQ4Marine»
2. Legg til kilder: filene i `kilder/skript/`, `kilder/pdf/`, `kilder/dokumenter/` og `kilder/kurs_README.md`. Forelesnings-PDF-ene kan også lastes opp direkte.
3. Studio-panelet: **Studieguide**, **Quiz**, **Flashcards** og **Lydoversikt** (fin på dårlige dager: lytt på tur).
4. Prompt å kopiere:

```text
Lag 8 eksamensoppgaver om korttidsekstremer (skript 07): 3 teori, 3 regning med tall og enheter, 2 om tolkning av kode.
Svar på norsk. Oppgi kilde for hvert løsningsforslag. Vis løsningene først når jeg skriver «fasit».
```

## Gemini Pro
1. https://gemini.google.com → **Gems** → ny Gem «UQ4Marine-veileder»
2. Last opp `kilder/_samlet_kurs.md`. Alt er samlet i én fil, så du sparer filplasser.
3. Instruks å kopiere:

```text
Du er veileder i Numerical Methods in UQ of Marine Applications. Bruk den opplastede filen som pensum.
Svar på norsk, kort og steg for steg, med SI-enheter. Gi hint før fasit. Si ifra når noe ikke står i pensum.
```

4. Bruk **Guided Learning** på nye begreper. Ta bilde av håndregningen din og be om retting.

## Perplexity Pro
1. https://www.perplexity.ai → **Spaces** → ny Space «UQ4Marine»
2. Instruks: `Akademiske kilder først. Oppgi standard, kapittel og år. Svar på norsk med engelske fagbegreper.`
3. Bruk den til å kryssjekke fakta fra Copilot og Gemini, og til eksterne kilder som Li, Gao & Moan (2013) og DNV-RP-C205.

## Notion
Lag én side «Eksamen UQ4Marine» med:
- Database **Pensum**: Tema · Skript · Status (Ikke startet / Påbegynt / Kan forklare) · Sist repetert (dato) · Vanskelig (avkrysning)
- Database **Feillogg**: Hva gikk galt · Riktig tankegang · Tema
- **Flashcards**: importer CSV fra `/kort` (Import → CSV)

## Én økt (45 min)
1. **Notion** (2 min): velg dagens tema.
2. **VS Code** (20 min): kjør skriptet celle for celle. Bruk `/forklar` på det som er uklart.
3. **VS Code** (10 min): endre én parameter. Forutsi resultatet først, kjør så.
4. **NotebookLM** (8 min): quiz på 5 spørsmål.
5. **Notion** (5 min): oppdater status og skriv én ting du ikke forsto.

**Lett dag (15 min):** `/lett-dag` i Copilot, *eller* en lydoversikt i NotebookLM. En liten økt teller også.

## Sikkerhet og regler
- Ikke last opp studentnummer, personnummer eller private dokumenter til KI-verktøy.
- Kursmateriale skal bare ligge i private notatbøker og repoer.
- Sjekk emnebeskrivelsen og HVL sine regler for KI-bruk før innleveringer og eksamen. Oppsettet er for **læring**, ikke for å levere KI-tekst.
