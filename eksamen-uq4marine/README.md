# Eksamen UQ4Marine: studieoppsett

VS Code, Copilot, NotebookLM, Gemini, Perplexity og Notion koblet sammen for emnet
*Numerical Methods in Uncertainty Quantification of Marine Applications*.
Kursfiler: https://github.com/Hugo-build/numerical_uq4marine_course

> ⚠️ **Først:** repoet denne mappen ligger i nå (`awesome_test-p-mc`) er **offentlig**.
> Ikke last opp kursmateriale hit. Flytt oppsettet til et **privat** repo på den nye kontoen (steg 1).

## Start (4 steg)

1. **Ny GitHub-konto + privat repo:** [guider/1-github-ny-konto.md](guider/1-github-ny-konto.md)
2. **Installer og sjekk alt med én kommando:**
   ```sh
   bash oppsett.sh
   ```
   Skriptet sjekker Git, installerer uv, henter kurset til `kurs/`, lager Python-miljøet, kjører leksjon 01 som test og installerer VS Code-utvidelsene. Det er trygt å kjøre på nytt, og en ny oppdatering vil bare oppdatere ting som er nødvendige.
3. **Åpne og kjør:**
   ```sh
   code .
   ```
   Åpne `kurs/pyscripts/01_vectors_matrices.py` → **Run Cell**. Copilot-oppsett: [guider/2-vscode-copilot.md](guider/2-vscode-copilot.md)

4. **Eksamenspakke til NotebookLM:** kjører alle kursskriptene og lager én PDF per tema (tekst, formler, kode, figurer) + kjørte notebooks:
   ```sh
   kurs/.venv/bin/python lag_notebooklm.py
   ```
   Last opp `kilder/notebooklm/` + slides fra Canvas. Se [guider/5-canvas-og-notebooklm.md](guider/5-canvas-og-notebooklm.md).

Reserve uten PDF-verktøy: `uv run lag_kilder.py` lager rene .md-filer. Se [guider/3-ai-verktoy.md](guider/3-ai-verktoy.md).
Vil du dobbel- eller trippelsjekke svar med Copilot, Claude, Codex, Perplexity og Grok? Se [guider/4-kryssjekk-flere-llm.md](guider/4-kryssjekk-flere-llm.md).

## Mappene

```text
eksamen-uq4marine/
├── oppsett.sh               ← kjør først (og når kurset er oppdatert)
├── lag_notebooklm.py        ← kjører kursskriptene → PDF per tema + .ipynb (NotebookLM, repetisjon)
├── lag_kilder.py            ← PDF + kursskript → .md for KI-verktøy (reserve)
├── pensum.md                ← temaer, fremdrift, eksamensspørsmål
├── eksamensplan.md          ← plan for alle eksamener H2026, med lagringspunkt
├── AGENTS.md                ← instruks og oppgaveliste for Codex
├── guider/                  ← 1 GitHub · 2 VS Code/Copilot · 3 KI-verktøy · 4 Kryssjekk · 5 Canvas → NotebookLM
├── notater/                 ← dine oppsummeringsark (_mal.md)
├── ovinger/                 ← dine kopier av skript og løsninger
├── materiale/               ← dine PDF-er (lastes ikke opp til GitHub)
├── kurs/                    ← forelesers repo, ikke endre (lages av oppsett.sh)
├── kilder/                  ← genererte filer: notebooklm/, notebooks/, animasjoner/ + .md-reserve
├── .github/copilot-instructions.md + prompts/   ← Copilot: norsk, hint før fasit, /forklar /oving …
├── .vscode/                 ← Python-tolk = kurs/.venv, anbefalte utvidelser
└── .vscode/settings.json    ← valgte innstillinger for Python og Copilot
```

## Hverdagen

| Økt | Hva |
|---|---|
| **Vanlig (45 min)** | Velg tema i `pensum.md`/Notion → kjør skriptet → `/forklar` → endre én parameter → quiz i NotebookLM → oppdater status |
| **Lett dag (15 min)** | `/lett-dag` i Copilot *eller* en lydoversikt i NotebookLM |
| **Lagre** | `git add . && git commit -m "notater" && git push` |

## Lett på disk (velg én)

| Valg | Plass | Hva |
|---|---|---|
| **1 · Ingenting lokalt** | ~0 | Last opp ferdige PDF-er til NotebookLM. Åpne `.ipynb` i Google Colab via Google Drive. Slett zip-filene etterpå. |
| **2 · Bare kurset** | lite | `bash oppsett.sh` uten pandoc/xelatex. Bruk ferdige PDF-er, kjør skriptene i VS Code. |
| **3 · Alt** | mest | Som 2 + `brew install pandoc` og LaTeX for å lage PDF-ene selv. Trengs bare hvis foreleser endrer kurset. |

Rydd: `rm -rf kilder/ && uv cache prune` (kurs/ og notatene dine blir liggende).

## Codex og andre kodeagenter
Les [AGENTS.md](AGENTS.md). Gi én oppgave om gangen, for eksempel:
`Les AGENTS.md. Gjør bare oppgave 1 (Sikkerhet) på en ny branch. Vis diff og resultatet av sjekkene. Ikke merge.`

## Hva er forbedret fra datalab-e-posten
- **Ett skript** i stedet for 7 manuelle steg. Det stopper med en tydelig melding hvis noe mangler.
- `uv sync --locked`: samme pakkeversjoner som foreleser (står i kursets README).
- **Mac:** Git krever `xcode-select --install`, og `code .` krever «Shell Command: Install 'code' command in PATH». Skriptet sier fra om begge.
- **Sikkerhet:** `curl … | sh` kjøres bare etter at du har sagt ja. Homebrew brukes hvis du har det.
- **Kurset ligger i `kurs/`, dine filer ved siden av.** Kursoppdateringer krasjer ikke med notatene dine.
- **Røyktest:** leksjon 01 kjøres automatisk, så du vet at alt virker før timen.

## AI, forståelse og håndkalkulasjon

### Hovedprinsipp
AI-verktøy som Claude, Codex, Copilot og lignende er nyttige til å:
- forklare konsepter
- generere kode
- lage struktur og plan
- sjekke beregninger og oppsummeringer

Men de kan også:
- gi feilaktige svar som ser overbevisende ut
- gjøre feil i antakelser om enheter, dimensjoner eller modellvalg
- feile i numerisk analyse uten at feilen alltid er tydelig
- produsere løsninger som ser riktige ut, men som ikke passer til problemet

Derfor er det viktig å kombinere AI med:
- matematisk forståelse
- håndkalkulasjon
- kritisk vurdering
- uavhengig verifisering av resultater

### Hvorfor håndkalkulasjon fortsatt er viktig
Håndkalkulasjon hjelper deg med å:
- bygge intuitiv forståelse for konseptet
- finne regnefeil tidlig
- vurdere om et tall er realistisk
- forstå antakelsene i modellen
- utvikle bedre prompts og bedre spørsmål til AI
- sette AI-output i riktig kontekst

Et godt arbeid flyter slik:
1. Forstå problemet matematisk
2. Gjør en enkel håndberegning eller skisse
3. Formuler modellen eller løsningsmetoden
4. Kjør beregningen i Python
5. Sjekk resultatet mot håndberegningen
6. Bruk AI til å forklare, forbedre og validere, ikke til å erstatte forståelsen

### Praktisk arbeidsflyt
#### 1. Før du skriver kode
- Les oppgaven nøye
- Identifiser hvilke størrelser som finnes
- Notér enheter og antakelser
- Skriv opp den enkleste varianten av problemet
- Finn forventet størrelsesorden på svaret

#### 2. Håndkalkulasjon
Gjennomfør minst ett av disse:
- enkel regning på papir
- beregning med håndholdte formler
- liten testcase hvor svaret er kjent
- kontroll av dimensjoner og enheter
- én kontrollregel som viser om resultatet er plausibelt

#### 3. Python-verifisering
- implementer modellen i Python
- bruk en liten, tydelig test
- sammenlign med håndkalkulasjonen
- sjekk om feilen er liten og forståelig

#### 4. AI-sjekk
Bruk Claude, Copilot, Codex eller andre verktøy for å:
- forklare hvordan løsningen virker
- foreslå forbedringer
- kontrollere logikken
- finne alternative formuleringer
- sammenligne ulike tilnærminger

Men du må fortsatt:
- lese svaret kritisk
- sjekke antakelser
- validere numerisk resultat

### Viktige temaer i dette emnet
Avhengig av kurset vil disse konseptene ofte være sentrale:
- vektorer og matriser
- lineære systemer
- numerisk stabilitet
- feilkilder og usikkerhet
- forventningsverdi og varians
- Monte Carlo-metoder
- sensitivitet og påvirkning av parametre
- diskretisering / finite-difference
- modellens antakelser og feilkilder

### God praksis for AI-bruk i numerisk arbeid
- Start med et tydelig, konkret spørsmål
- Bruk små, fokuserte prompts
- Be om forklaring før fasit
- Be om verifisering av antakelser
- Be om edge cases og feilsituasjoner
- Be om kontroll av enheter og dimensjoner
- Be om sammenligning av flere metoder
- Kjør alltid en enkel sanity check selv om AI har generert kode

### Kort plan for deg
#### Uke 1: Forståelse
- velg ett tema fra pensum
- les det grundig
- skriv ned 3–5 viktige definisjoner
- gjør én enkel håndberegning

#### Uke 2: Modell og kode
- skriv en liten Python-implementasjon
- test på kjent eksempel
- sammenlign med håndberegningen

#### Uke 3: Verifisering og kritisk vurdering
- bruk AI til å forklare og forbedre
- sammenlign flere svar
- dokumentér feil, antakelser og begrensninger

#### Uke 4: Finalisering
- skriv oppsummering
- legg ved håndregninger og kontrollpunkter
- forklar hvorfor resultatet er plausibelt
- reflekter over hvor AI hjalp, og hvor menneskelig skjønn var nødvendig

### Enkel sjekkliste før innlevering
- [ ] Jeg forstår konseptet uten å bare stole på AI
- [ ] Jeg har gjort minst én håndberegning
- [ ] Jeg har verifisert resultatet med Python
- [ ] Jeg har sjekket enheter, dimensjoner og størrelsesorden
- [ ] Jeg har vurdert om resultatet er plausibelt
- [ ] Jeg har brukt AI som verktøy, ikke som eneste kilde til sannhet
- [ ] Jeg kan forklare hvorfor løsningen er riktig

### Oppsummering
Det viktigste læringsmålet er ikke bare å få et numerisk svar. Det er å kunne:
- gjøre en liten, forståelig beregning selv
- bruke AI som støtte
- kontrollere output kritisk
- forstå hvorfor resultatet er riktig eller feil

Dette er også den viktigste sikkerheten mot AI-feil, dårlig prompting og numeriske misforståelser.

---

## GitHub + Claude + Codex workflow

For en effektiv og trygg arbeidsflyt på GitHub er det best å dele arbeidet slik:

- **Claude**: planlegging, arkitektur, UX, kritisk vurdering, review
- **Codex**: implementasjon, små patcher, API-ruter, kodegenerering
- **GitHub**: oppgaver, branches, PR-er og dokumentasjon

### Praktisk prosess
1. Opprett en issue for én liten oppgave
2. Lag en branch for oppgaven
3. Be Claude om en kort teknisk plan
4. La Codex implementere kun det som trengs
5. Review PR-en og sjekk om resultater er plausible
6. Merge først når koden er validert og forstått

### God praksis
- Hold prompts små og fokuserte
- Endre kun ett felt/fil om gangen
- Be om liten, presis kode, ikke full rewrite
- Be om verifisering av edge cases
- Ikke bruk AI som eneste kontrollmekanisme
- Sjekk alltid numerisk plausibilitet selv om AI sier at det er riktig

I praksis er dette den tryggeste måten å bruke AI uten å brenne tokens eller gi opp forståelsen.
