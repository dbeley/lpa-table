# lpa-table

An alternative front-end for the data hosted at [LinuxPhoneApps.org](https://linuxphoneapps.org/).

## Usage

The data should be re-generated every monday.

If you want to manually create an export:

- Copy `.env.example` to `.env` and fill it with your own tokens.
- `python lpa_table_export.py`: will create `export.csv` containing F-Droid apps data.
- `python lpa_html_builder.py`: will create `docs/index.html` with `export.csv` and `template.html`.

## External data

- Github: number of stars, forks
- Gitlab : number of stars, forks
- Codeberg : number of stars, forks

# Credits

- [https://linuxphoneapps.org/](https://framagit.org/linuxphoneapps/linuxphoneapps.frama.io)
