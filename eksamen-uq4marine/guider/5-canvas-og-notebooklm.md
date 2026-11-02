# 5 · Canvas-slides + kursskript → NotebookLM → eksamen

Tid: 20–30 min første gang. Etterpå er alt klart for quiz, flashcards, slides og lydoversikt.

## A. Hent slides fra Canvas (velg det som virker)

1. **Hele emnet på én gang** (hvis UiS har det slått på)
   Konto (profilbildet) → **Innstillinger** → **Last ned emneinnhold** → velg emnet → **Generer ePub** → vent → **Last ned tilknyttede filer**.
   Du får en zip med slides og lesestoff. Filer foreleser har skjult, er ikke med.
   *Engelsk meny:* Account → Settings → Download Course Content → Generate ePub → Download Associated Files.
2. **Filer-siden:** emnet → **Filer** → huk av alle → **Last ned** (zip). Mangler «Filer» i menyen? Da er den skjult, bruk punkt 3.
3. **Moduler:** åpne hver forelesning og last ned PDF/PPTX én og én.

Pakk ut i `materiale/`. `.gitignore` hindrer at kursmaterialet havner på GitHub.

## B. Lag notatboken

1. https://notebooklm.google.com → **Ny notatbok** «UQ4Marine eksamen»
2. Dra inn som kilder:
   - **alt i `kilder/notebooklm/`**: én PDF per tema (tekst, formler, kode, figurer), oversikt med eksamensspørsmål, og metocean-artikkelen
   - **slides fra Canvas:** PDF og PPTX kan lastes opp direkte. Gammel `.ppt` → lagre som PDF først. Passordbeskyttede PDF-er virker ikke.
   - **gamle eksamener og øvinger** fra Canvas, hvis de finnes (mest verdt av alt)
3. Grense: 50 kilder per notatbok på gratisplanen. Du bruker ca. 15 + slides.
4. Chat-innstillinger → egendefinert stil, lim inn:

```text
Du er eksamensveileder i Numerical Methods in Uncertainty Quantification of Marine Applications (UiS).
Svar på norsk, kort og steg for steg. Engelske fagbegreper i parentes første gang. SI-enheter.
Bruk bare kildene i notatboken og vis kildehenvisning. Si tydelig fra når noe ikke står i kildene.
Gi hint før fasit. Skill alltid mellom momentanrespons, korttidsmaksimum (3 timer) og årsmaksimum.
```

## C. Studio: slides og øving (kopier og lim inn)

**Lysbildeserie (Slide Deck):** Studio → Slide Deck → velg bare kildene for ett tema → språk norsk → egendefinert prompt:

```text
Repetisjonsslides for eksamen, tema 07 korttidsekstremer. 10–12 slides.
Én idé per slide: definisjon, formel med symbolforklaring og enheter, typisk eksamensfelle.
Bruk figurene fra kildene der det passer. Siste slide: 5 kontrollspørsmål uten svar.
```

Bytt ut temaet for hver blokk i eksamensplanen. Last ned som PDF eller PPTX fra ⋮-menyen.
⚠️ Slides er KI-laget og kan ha feil. Sjekk formler mot PDF-ene før du pugger dem.

**Quiz:**

```text
10 spørsmål om tema 05–08. 4 om begreper, 4 med tall og enheter, 2 om å tolke en figur. Eksamensnivå.
```

**Flashcards:**

```text
Alle formler og definisjoner i kildene. Forside: navn eller situasjon. Bakside: formel, symboler, enheter og når den gjelder.
```

**Lydoversikt (dårlige dager, lytt på tur):**

```text
Forklar korttids- og langtidsekstremer (07–08) for en maskiningeniør som har vært borte fra matte en stund.
Rolig tempo, konkrete eksempler med semi-rig og en 3-timers storm.
```

**Rapport → formelark:**

```text
Formelark på maks 2 sider: Normal, Rayleigh, Rayleigh-n, Gumbel, Weibull, lognormal; JONSWAP og spektralmomenter;
DAF og fase; Monte Carlo-feil og konvergens. Kildehenvisning på hver formel.
```

**Prøveeksamen (i chatten):**

```text
Lag en prøveeksamen på 3 timer i stil med de sju eksamensspørsmålene i 00_oversikt. 4 oppgaver med deloppgaver,
minst én med håndregning. Ikke vis fasit før jeg skriver «fasit». Rett svarene mine med kildehenvisning.
```

## D. Når foreleser oppdaterer kurset

```sh
bash oppsett.sh && kurs/.venv/bin/python lag_notebooklm.py
```

NotebookLM oppdaterer ikke opplastede filer selv: slett de gamle kildene og last opp de nye.

## Trygt og lurt

- Hold notatboken privat. Ingen studentnummer eller personinfo i kilder eller chat.
- KI er nesten alltid forbudt på selve eksamen. Dette er for å **lære**: gjør minst én håndregning per tema.
- Uenig med NotebookLM? Kryssjekk: [4-kryssjekk-flere-llm.md](4-kryssjekk-flere-llm.md)
