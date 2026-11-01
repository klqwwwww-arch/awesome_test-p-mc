# 4 · Kryssjekk med flere KI-er + repo: hvorfor og hvordan

> Kort versjon: **én KI løser, to sjekker blindt, koden dømmer.** Repoet er stedet der alt dette bor.
> I dette oppsettet: legg sjekk-skript i `ovinger/`, bruk `/sjekk` i Copilot og `uv run lag_kilder.py` for kildene.

## 1. Hvorfor flere KI-er? (poeng og hensikt)

- En KI kan ta feil **med full selvtillit**. Den samme feilen to ganger på rad fra samme KI beviser ingenting.
- To **uavhengige** KI-er som kommer frem til samme tall uten å se hverandres svar gir mye høyere tillit.
- Men KI-er er trent på mye av det samme og kan gjøre **samme feil**. Derfor er det **formelark, pensum og et Python-skript** som dømmer, ikke flertallet.
- **Uenighet er gull:** der KI-ene er uenige, finner du stedet du må forstå. Det er der læringen skjer.

## 2. Hvorfor repo? (poeng, hensikt, fordeler)

| Fordel | Hva det betyr i praksis |
|---|---|
| **Én kilde til sannhet** | Kontekstfiler (`.github/copilot-instructions.md`, `pensum.md`) og kontrolltall ligger ett sted. Alle KI-er får samme kontekst, så du slipper å forklare på nytt |
| **KI-ene leser selv** | Copilot, Claude Code og Codex leser filene i repoet direkte. Mindre kopiering og liming |
| **Kjørbar fasit** | Sjekk-skriptet (`sjekk_*.py`) regner alt på nytt på sekunder. Tall du kan stole på, ikke tall noen *sa* |
| **Historikk** | Git viser hva som ble endret og når. Du kan alltid gå tilbake |
| **Backup og synk** | Privat repo på GitHub: Mac, skolemaskin og nett har samme filer |
| **Sikkerhet** | Privat repo, og `.gitignore` holder PDF-er og hemmeligheter ute |

## 3. Hvem gjør hva

| Verktøy | Rolle i sjekken | Typisk spørsmål |
|---|---|---|
| **Claude** | Hovedløsning, utledning, forklaring | «Utled og forklar steg for steg» |
| **VS Code + Copilot** | Kjør sjekk-skriptet, forklar koden, `/sjekk` på din egen løsning | «Kjør skriptet og forklar linje 40» |
| **Codex** (OpenAI) | Uavhengig **kode**: skriver sitt eget skript fra oppgaveteksten | «Skriv Python som regner dette fra bunnen» |
| **Perplexity** | **Kilder**: er formelen eller antakelsen standard? (DNV, lærebøker) | «Hvilken standard sier at 3 t er referansevarighet?» |
| **Grok** | Ekstra uavhengig **tall**-sjekk eller annen forklaring | «Løs deloppgave 3.4 selv» |
| **NotebookLM** | Pensum-sjekk med sidehenvisning | «Hvor i kompendiet står dette?» |

## 4. Arbeidsflyt: blind sjekk i 4 steg

1. **Fasit først:** ha kontrolltallene klare (egen håndregning eller sjekk-skript). **Ikke** vis dem til KI-en.
2. **Blindt:** gi samme deloppgave til 2 KI-er hver for seg (prompt under). De regner selv.
3. **Sammenlign** mot kontrolltabellen. Innenfor ±1 % → ✅. Uenige → steg 4.
4. **Dommer:** kjør sjekk-skriptet og sjekk formelarket. Finn **hvorfor** den ene tar feil. Skriv det i feilloggen (Notion).

```text
Steg 1        Steg 2                 Steg 3              Steg 4
fasit ──► KI-A blindt ──┐
                        ├──► sammenlign ──► uenig? ──► skript + formelark ──► feillogg
          KI-B blindt ──┘          │
                                   └──► enig ✅
```

### Blind-prompt (kopier)
```text
Solve this independently. Show the formula, the numbers inserted and the result with units.
State your assumptions. Do not look up solutions online.
Task: <paste the sub-question>
```

### Sammenlign-prompt (etter at den har svart)
```text
My control values are: <paste>. Where do you disagree with them, and why?
Point out who is wrong, with a reason (formula, unit, assumption).
```

### Codex-prompt (uavhengig kode)
```text
Write a short Python script (numpy/scipy) that computes every number asked for in this task from scratch.
Print each result with units. Do not use any values other than those given in the task.
Task: <paste>
```

## 5. Regler

- **Maks 3 verktøy per deloppgave.** Ellers bruker du energien på å sjekke dem som sjekker.
- **Hvem vinner ved uenighet:** pensum/formelark > Python-skript > flertall av KI-er.
- **Personvern:** aldri studentnr., e-post eller helseinfo. Kurs-PDF-er bare i private verktøy og private repoer.
- **Kostnad:** bruk det du allerede har. Ikke kjøp nye abonnement for dette.
- **Eksamen er uten KI.** Sjekken er for læring. Skriv innleveringer slik emnet krever, og oppgi KI-bruk når det kreves.

## 6. Etter energinivå

| Dag | Oppsett |
|---|---|
| Tung | Claude + skriptet. Ferdig |
| Normal | + Copilot på det du er usikker på |
| God | Trippelsjekk: Claude + Codex/Grok blindt + skriptet som dommer |
