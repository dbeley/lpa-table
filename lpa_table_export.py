import logging
import os
import tomllib
from pathlib import Path

import pandas as pd
from github import Github
from gitlab import Gitlab

from utils import (
    get_codeberg_repository_data,
    get_github_repository_data,
    get_gitlab_repository_data,
    get_gitlab_repository_data_with_webscraping,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s :: %(message)s")
logger = logging.getLogger(__name__)

REPOSITORY_APIS = {
    "github.com": Github(os.environ.get("GITHUB_TOKEN")),
    "gitlab.com": Gitlab(private_token=os.environ.get("GILAB_TOKEN")),
    "invent.kde.org": Gitlab(
        url="https://invent.kde.org", private_token=os.environ.get("GILAB_KDE_TOKEN")
    ),
}
IGNORED_FILES = ["_index.md"]


def _extract_repository_name(repository: str, repository_domain: str) -> str:
    repository_name = (
        repository.split("://")[-1].split(f"{repository_domain}/")[-1].strip("/")
    )
    if repository_name.count("/") > 1:
        repository_name = (
            repository_name.split("/")[0] + "/" + repository_name.split("/")[1]
        )
    return repository_name


def _get_repository_stats(repository: str, repository_domain: str) -> dict[str, str]:
    if not repository:
        return {}
    repository_name = _extract_repository_name(repository, repository_domain)
    match repository_domain:
        case "github.com":
            return get_github_repository_data(
                REPOSITORY_APIS["github.com"], repository_name
            )
        case "codeberg.org":
            return get_codeberg_repository_data(repository_name)
        case "gitlab.com":
            return get_gitlab_repository_data(
                REPOSITORY_APIS["gitlab.com"], repository_name
            )
        case "invent.kde.org":
            return get_gitlab_repository_data(
                REPOSITORY_APIS["invent.kde.org"], repository_name
            )
        case "gitlab.gnome.org" | "source.puri.sm" | "gitlab.manjaro.org":
            return get_gitlab_repository_data_with_webscraping(repository)
    return {}


list_files = Path("linuxphoneapps.frama.io/content/apps").glob("**/*.md")
list_data = []
for index, file in enumerate(list_files, 1):
    if str(file.name) in IGNORED_FILES:
        continue
    logger.info(str(file))
    with file.open() as f:
        data = [line for line in f.readlines()]
    app_config = tomllib.loads("".join(data).split("+++")[1])

    repository = app_config.get("extra", {}).get("repository")
    repository_domain = repository.split("://")[1].split("/")[0] if repository else ""
    repository_stats = _get_repository_stats(repository, repository_domain)
    app_id = app_config.get("extra", {}).get("app_id")
    if len(app_config.get("taxonomies", {}).get("mobile_compatibility", [])) > 1:
        logger.warning("More than one item in mobile_compatibility")
    mobile_compatibility = (
        app_config.get("taxonomies", {}).get("mobile_compatibility", [])[0].title()
    )
    frameworks = ", ".join(app_config.get("taxonomies", {}).get("frameworks", []))
    categories = ", ".join(
        [
            word.title()
            for word in app_config.get("taxonomies", {}).get("categories", [])
        ]
    )
    # breakpoint()

    list_data.append(
        {
            "name": app_config.get("title", ""),
            "url": f"https://linuxphoneapps.org/apps/{app_id}",
            "repository": repository,
            **repository_stats,
            "repository_domain": repository_domain,
            "description": app_config.get("description"),
            "categories": categories,
            "compatibility": mobile_compatibility,
            "frameworks": frameworks,
            "created": app_config.get("date"),
            "last_updated": app_config.get("updated"),
        }
    )

df = pd.DataFrame.from_records(list_data)
df = df.astype(
    {
        "repository_stars_count": "Int64",
    }
)
df = df.sort_values(by=["name"])
df.to_csv("export.csv", index=False)
