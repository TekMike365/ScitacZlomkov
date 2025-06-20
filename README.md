# Sčítač Zlomkov

Jednoduchý program na sčítanie zlomkov.

Stiahnuť ho môžete [tu](https://github.com/TekMike365/ScitacZlomkov/releases) alebo
ho môžete skompilovať podľa [inštrukcií nižšie](#kompilácia-windows).

## Development

### Nastavenie virtuálneho prostredia

1. Ak nemáte v pythone modul `venv` stiahnite ho pomocou

```sh
pip install venv
```

2. Vytvorte virtuálne prostredie a aktivujte ho

```sh
python3 -m venv .venv
source .venv/bin/activate
```

> Deaktivovať virtuálne prostredie môžete s pomocou príkazu: `deactivate`

3. Nainštalujte vyžadované moduly

```sh
pip install -r requirements.txt
```

4. Spustite program :D

```sh
python scitac_zlomkov.py
```

### Kompilácia (Windows)

Pre skompilovanie Sčítača Zlomkovov treba najprv nastaviť [virtuálne prostredie](#nastavenie-virtuálneho-prostredia).

```sh
pyinstaller -F scitac_zlomkov.py -n ScitacZlomkov.exe
```
