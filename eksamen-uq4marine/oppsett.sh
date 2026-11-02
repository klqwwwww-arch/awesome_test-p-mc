#!/usr/bin/env bash
# Oppsett for datalab + eksamensforberedelse (macOS, virker også på Linux).
# Trygt å kjøre flere ganger: sjekker alt, installerer det som mangler og oppdaterer kurset.
#
# Bruk (fra mappen eksamen-uq4marine):   bash oppsett.sh
set -euo pipefail

KURS_URL="https://github.com/Hugo-build/numerical_uq4marine_course.git"
ROT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KURS="$ROT/kurs"
cd "$ROT"

ok()    { printf '  ✅ %s\n' "$*"; }
obs()   { printf '  ⚠️  %s\n' "$*"; }
stopp() { printf '  ❌ %s\n' "$*"; exit 1; }
steg()  { printf '\n▶ %s\n' "$*"; }

steg "1/6 Git"
# På macOS finnes /usr/bin/git alltid, men feiler til Command Line Tools er installert.
if git --version >/dev/null 2>&1; then
    ok "$(git --version)"
else
    stopp "Git mangler. Kjør:  xcode-select --install   – og kjør  bash oppsett.sh  på nytt."
fi

steg "2/6 uv (pakkebehandler for Python)"
if ! command -v uv >/dev/null 2>&1; then
    if command -v brew >/dev/null 2>&1; then
        obs "uv mangler – installerer med Homebrew"
        brew install uv
    else
        obs "uv mangler. Offisiell installer: https://astral.sh/uv/install.sh"
        read -r -p "  Laste ned og kjøre den nå? [j/N] " svar || svar=""
        case "$svar" in
            [jJyY]*) curl -LsSf https://astral.sh/uv/install.sh | sh ;;
            *) stopp "Avbrutt. Installer uv selv (https://docs.astral.sh/uv/) og kjør skriptet på nytt." ;;
        esac
        # Gjør uv tilgjengelig i dette vinduet uten å åpne ny terminal
        export PATH="$HOME/.local/bin:$PATH"
    fi
fi
ok "$(uv --version)"

steg "3/6 Kursrepo (forelesers filer) → kurs/"
if [ -d "$KURS/.git" ]; then
    if git -C "$KURS" pull --ff-only --quiet; then
        ok "Oppdatert til nyeste versjon"
    else
        obs "Fikk ikke oppdatert kurs/. Har du endret filer der? Egne endringer hører hjemme i ovinger/."
    fi
else
    git clone --quiet "$KURS_URL" "$KURS"
    ok "Klonet til kurs/"
fi

steg "4/6 Python-miljø (uv sync --locked → kurs/.venv)"
if ! (cd "$KURS" && uv sync --locked --quiet); then
    obs "Låsefilen passer ikke med pyproject.toml – prøver vanlig  uv sync"
    (cd "$KURS" && uv sync --quiet)
fi
ok "$("$KURS/.venv/bin/python" -c 'import sys, numpy, scipy, matplotlib; print(f"Python {sys.version.split()[0]} · numpy {numpy.__version__} · scipy {scipy.__version__} · matplotlib {matplotlib.__version__}")')"

steg "5/6 Røyktest: kjører leksjon 01 uten plottvinduer"
if (cd "$KURS" && MPLBACKEND=Agg uv run --quiet python pyscripts/01_vectors_matrices.py >/dev/null); then
    ok "01_vectors_matrices.py kjører"
else
    obs "Leksjon 01 feilet – ta med feilmeldingen over til datalab."
fi

steg "6/6 VS Code + utvidelser"
CODE=""
MAC_CODE="/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
if command -v code >/dev/null 2>&1; then
    CODE="code"
elif [ -x "$MAC_CODE" ]; then
    CODE="$MAC_CODE"
    obs "Tips: VS Code → Cmd+Shift+P → «Shell Command: Install 'code' command in PATH»"
fi
if [ -n "$CODE" ]; then
    for ext in ms-python.python ms-toolsai.jupyter github.copilot-chat; do
        if "$CODE" --install-extension "$ext" >/dev/null 2>&1; then ok "$ext"; else obs "Fikk ikke installert $ext"; fi
    done
else
    obs "Fant ikke VS Code. Last ned: https://code.visualstudio.com/download – kjør skriptet på nytt etterpå."
fi

printf '\n🎉 Ferdig. Neste steg:\n'
printf '   1) code "%s"\n' "$ROT"
printf '   2) Åpne kurs/pyscripts/01_vectors_matrices.py → klikk «Run Cell» over første # %%%%\n'
printf '   3) Eksamenspakke: kurs/.venv/bin/python lag_notebooklm.py   (PDF per tema → NotebookLM, se guider/5)\n'
printf '      Uten pandoc/xelatex: uv run lag_kilder.py   (rene .md-filer)\n'
