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

### Tokens

The weekly refresh (`.github/workflows/refresh_data.yaml`) reads three repository
secrets: `GITHUB_TOKEN` (provided by Actions), `GITLAB_TOKEN` (gitlab.com) and
`GITLAB_KDE_TOKEN` (invent.kde.org).

The GitLab tokens only raise rate limits. If one is missing, expired or revoked, the
export logs a warning and keeps going through unauthenticated access to the public
instances, so the table is still refreshed instead of failing entirely.

## External data

- Github: number of stars, last repo update
- Gitlab (gitlab.com, invent.kde.org instances): number of stars, last repo update
- Other Gitlab instances (gitlab.gnome.org, source.puri.sm, gitlab.manjaro.org): number of stars, through the GitLab API
- Codeberg: number of stars, last repo update
- SourceHunt: last repo update

# Credits

- [https://linuxphoneapps.org/](https://framagit.org/linuxphoneapps/linuxphoneapps.frama.io)
