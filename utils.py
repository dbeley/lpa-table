import calendar
import logging
import os
import time

import requests
from datetime import datetime
from github import Github
from github.GithubException import RateLimitExceededException, UnknownObjectException
from gitlab import Gitlab
from gitlab.exceptions import GitlabError, GitlabGetError
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def _warn_actions(message: str) -> None:
    """Surface the warning in the Actions UI, not only in the job logs."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::warning::{message}", flush=True)


def build_gitlab_client(url: str, private_token: str | None) -> Gitlab:
    """Build a GitLab client, validating the token first.

    A missing, expired or revoked token must not abort the whole export: we fall
    back to an unauthenticated client, which still reads public projects.
    """
    if not private_token:
        return Gitlab(url)
    try:
        client = Gitlab(url, private_token=private_token)
        client.auth()
    except GitlabError as error:
        message = (
            f"GitLab token rejected by {url} ({error}). "
            "Falling back to unauthenticated access: only public projects will be read. "
            "Renew the token and the repository secret."
        )
        logger.warning(message)
        _warn_actions(message)
        return Gitlab(url)
    return client


def get_github_repository_data(g: Github, repository_name: str):
    try:
        repo = g.get_repo(repository_name)
    except UnknownObjectException:
        logger.warning(f"Repository {repository_name} was not found on Github.")
        return {}
    except RateLimitExceededException:
        core_rate_limit = g.get_rate_limit().core
        reset_timestamp = calendar.timegm(core_rate_limit.reset.timetuple())
        sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 10
        logger.warning(f"Rate-limit detected, sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        repo = g.get_repo(repository_name)
    return {
        "repository_stars_count": repo.stargazers_count,
        "repository_last_update": int(repo.updated_at.timestamp()),
    }


def get_gitlab_repository_data(gl: Gitlab, repository_name: str):
    try:
        repo = gl.projects.get(repository_name)
        last_commit_date = repo.commits.list(per_page=1, get_all=False)[
            0
        ].committed_date
    except GitlabGetError:
        logger.warning(f"Repository {repository_name} was not found on Gitlab.")
        return {}
    except GitlabError as error:
        # A single unreadable project (auth, rate-limit, empty repository) must
        # not abort the whole export.
        logger.warning(f"Couldn't read {repository_name} on Gitlab: {error}")
        return {}
    return {
        "repository_stars_count": repo.star_count,
        "repository_last_update": int(
            datetime.strptime(last_commit_date[0:10], "%Y-%m-%d").timestamp()
        ),
    }


def get_gitlab_repository_data_with_webscraping(repository_url: str):
    try:
        soup = BeautifulSoup(requests.get(repository_url).content, "lxml")
        repository_stars_count = int(
            soup.select("a.gl-button.star-count")[0].text.strip()
        )
        return {
            "repository_stars_count": repository_stars_count,
        }
    except Exception as e:
        logger.warning(f"Couldn't scrape {repository_url}: {e}")
        return {}


def get_codeberg_repository_data(repository_name: str):
    result = requests.get(f"https://codeberg.org/api/v1/repos/{repository_name}")
    if result.status_code == 200:
        json_result = result.json()
        return {
            "repository_stars_count": json_result.get("stars_count"),
            "repository_last_update": int(
                datetime.strptime(
                    json_result.get("updated_at")[0:10], "%Y-%m-%d"
                ).timestamp()
            ),
        }
    return {}


def get_sourcehunt_repository_data_with_webscraping(repository_url: str):
    try:
        soup = BeautifulSoup(requests.get(repository_url).content, "lxml")
        commit_list = soup.select("small.pull-right a span")
        if len(commit_list) >= 1:
            repository_last_update = int(
                datetime.strptime(
                    commit_list[0].get("title")[0:10], "%Y-%m-%d"
                ).timestamp()
            )
            return {
                "repository_stars_count": 0,  # sourcehunt doesn't support starring projects
                "repository_last_update": repository_last_update,
            }
        return {}
    except Exception as e:
        logger.warning(f"Couldn't scrape {repository_url}: {e}")
        return {}
