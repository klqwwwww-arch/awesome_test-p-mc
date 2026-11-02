# 1 · Ny GitHub-konto + privat repo

Tid: ca. 20 min. Hvorfor: repoet `awesome_test-p-mc` er **offentlig**. Kursmateriale og notater bør ligge i et **privat** repo.

## A. Lag kontoen

1. Gå til https://github.com/signup
   - Bruk skole-e-posten din, så går studentverifiseringen raskere.
   - Brukernavn uten fullt navn eller fødselsår.
2. Slå på totrinnsinnlogging: https://github.com/settings/security
   - Velg passkey eller autentiseringsapp. Lagre gjenopprettingskodene i passordbehandleren.
3. Skjul e-posten: https://github.com/settings/emails
   - Huk av «Keep my email addresses private».
   - Kopier `…@users.noreply.github.com`-adressen. Den trenger du i steg C.
4. Søk om studentfordeler (gratis Copilot for studenter): https://education.github.com/pack
   - Last opp studentbevis eller bruk skole-e-post. Godkjenning kan ta noen dager.

## B. Logg inn fra Mac-en (velg ett alternativ)

**Alternativ 1, enklest: GitHub CLI**

```sh
brew install gh
gh auth login          # GitHub.com → HTTPS → Login with a web browser
gh auth setup-git      # git bruker gh-innloggingen
```

Har du allerede den gamle kontoen innlogget? `gh auth login` legger til den nye. Bytt med:

```sh
gh auth status
gh auth switch
```

**Alternativ 2: SSH-nøkkel (egen nøkkel for den nye kontoen)**

```sh
ssh-keygen -t ed25519 -C "github-ny" -f ~/.ssh/id_ed25519_github_ny   # velg en passfrase
pbcopy < ~/.ssh/id_ed25519_github_ny.pub                                # lim inn på https://github.com/settings/keys
```

Legg dette i `~/.ssh/config`:

```text
Host github-ny
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github_ny
  IdentitiesOnly yes
  AddKeysToAgent yes
  UseKeychain yes
```

Test: `ssh -T git@github-ny`. Bruk så `git@github-ny:BRUKERNAVN/eksamen-uq4marine.git` som remote-adresse.

## C. Flytt oppsettet til et nytt privat repo

Bytt ut `DITT NAVN` og `NOREPLY-ADRESSE`. Resten kan kopieres som det står.

```sh
mkdir -p ~/Studie && cd ~/Studie
git clone --depth 1 --branch main https://github.com/klqwwwww-arch/awesome_test-p-mc.git _midlertidig
cp -R _midlertidig/eksamen-uq4marine ./eksamen-uq4marine
rm -rf _midlertidig
cd eksamen-uq4marine

git init -b main
git config user.name "DITT NAVN"
git config user.email "NOREPLY-ADRESSE"
git add .
git commit -m "Oppsett for eksamen"
gh repo create eksamen-uq4marine --private --source=. --remote=origin --push

bash oppsett.sh
```

- `git config` uten `--global` gjelder bare dette repoet, så den gamle kontoen påvirkes ikke.
- Valgte du SSH? Bytt `gh repo create …` med: lag et tomt privat repo på https://github.com/new, deretter
  `git remote add origin git@github-ny:BRUKERNAVN/eksamen-uq4marine.git && git push -u origin main`.

## D. Daglig lagring

```sh
git add . && git commit -m "Notater uke X" && git push
```

## Sjekkliste
- [ ] Ny konto, 2FA på, e-post skjult
- [ ] Studentfordeler søkt
- [ ] Privat repo `eksamen-uq4marine` opprettet og pushet
- [ ] `bash oppsett.sh` kjørt uten ❌
