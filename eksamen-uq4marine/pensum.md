# Pensum og fremdrift

Bytt ⬜ → 🟨 (påbegynt) → ✅ (kan forklare uten hjelp). Rekkefølgen følger filnavnene i `kurs/pyscripts/`.

| Status | # | Tema | Kjerne |
|---|---|---|---|
| ⬜ | 01 | Vektorer og matriser | `@` vs `*`, lineære systemer, egenpar, minste kvadrater |
| ⬜ | 02 | Sannsynlighetsmodeller | Normal, Rayleigh, Rayleigh-n, Gumbel, Weibull, lognormal, tilpasning |
| ⬜ | 03-1 | Statisk stav, fagverk, bjelke | Stivhet, sammenstilling, Euler–Bernoulli |
| ⬜ | 03-2 | Monte Carlo på fagverk | Usikker last/E/A, overskridelse, konvergens |
| ⬜ | 03-3 | 3D-fagverk | Lokal→global, egenmoder, Newmark-β vs RK4 |
| ⬜ | 03-4 | Hul sylinder (skall) | Q4-skall, membran + bøying, MITC4 |
| ⬜ | 03-5 | Massiv sylinder (T4) | 3D-elastisitet, spenninger, patch-test |
| ⬜ | 04 | Lineær dynamikk og DAF | SDOF, dynamisk forsterkning, fase, transient |
| ⬜ | 05 | Metocean-statistikk | Vind–Hs–Tp-modell, IFORM, 50-års kontur |
| ⬜ | 06 | JONSWAP-bølger | Spektrum, Hm0 = 4√m0, retningsspredning |
| ⬜ | 07 | Korttidsekstremer | 3-timers maks, Gumbel, Rayleigh/Rice-topper |
| ⬜ | 08 | Langtidsfordelinger | Hs–Tp-rutenett, blandingsfordeling, årsmaks |

## Spørsmål du bør kunne svare på
Fra forelesers README («Instructor prompts»). Svar muntlig eller i `notater/`.

1. Forklar `*`, `@`, ytreprodukt og broadcasting før du regner.
2. Hvordan flytter kvantilene for Rayleigh-maksimum seg når n øker?
3. Finn stivlegememodene før du legger på randbetingelser.
4. Skill transient respons fra stasjonær harmonisk respons.
5. Sammenlign samplingsfeil med usikkerheten i fysiske input.
6. Hvorfor kan ikke marginalfordelingen av tidssampler alene bestemme maksimum i en tidsserie?
7. Hvorfor er en blanding av blokkmaksima ikke en årsmaksimumsfordeling?

## Tre fordelinger som ikke må blandes
- **Momentanrespons**: én tilfeldig verdi, ev. betinget på miljø.
- **Korttidsmaksimum**: maks over en gitt varighet (f.eks. 3 t), med tidsavhengighet.
- **Årsmaksimum**: maks over et år med miljøblokker, med en eksplisitt aggregeringsmodell.
