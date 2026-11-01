# Øvinger

Kopier et kursskript hit **før** du endrer det. Da er forelesers fil uendret, og `bash oppsett.sh` kan oppdatere kurset.

```sh
cp kurs/pyscripts/04_linear_dynamics_daf.py ovinger/
```

Kjør i VS Code med «Run Cell» (tolk: `kurs/.venv`), eller i terminalen:

```sh
uv run --project kurs python ovinger/04_linear_dynamics_daf.py
```

Skript `03-3_3d_truss.py` trenger også geometrien:

```sh
cp -R kurs/pyscripts/40barTruss ovinger/
```
