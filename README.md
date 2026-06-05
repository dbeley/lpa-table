# lpa-table

An alternative front-end for the data hosted at [LinuxPhoneApps.org](https://linuxphoneapps.org/).

## Usage

```
git submodule init
git submodule update
```

The data should be re-generated every monday.

If you want to manually create an export:

- Copy `.env.example` to `.env` and fill it with your own tokens.
- `python lpa_table_export.py`: will create `export.csv` containing F-Droid apps data.
- `python lpa_html_builder.py`: will create `docs/index.html` with `export.csv` and `template.html`.

## External data

- Github: number of stars, last repo update
- Gitlab (gitlab.com, invent.kde.org instances): number of stars, last repo update
- Other Gitlab instances: number of stars
- Codeberg: number of stars, last repo update
- SourceHunt: last repo update

# Credits

- [https://linuxphoneapps.org/](https://framagit.org/linuxphoneapps/linuxphoneapps.frama.io)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for bugs, features, or documentation improvements.

### Development

1. Clone the repository with submodules:
   ```bash
   git clone --recurse-submodules https://github.com/dbeley/lpa-table
   cd lpa-table
   ```
2. Copy `.env.example` to `.env` and add your API tokens
3. Run `python lpa_table_export.py` to generate data
4. Run `python lpa_html_builder.py` to generate the website

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
