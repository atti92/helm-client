import subprocess
from typing import List

import pydantic
from pydantic import AnyUrl

from helm.common import helm_run, normalize_args

from .models import HelmRepo


class OciUrl(AnyUrl):
    allowed_schemes = {"oci"}

    __slots__ = ()


def subcommand_run(*args, **kwargs):
    return helm_run("repo", *args, **kwargs)


def add(
    helm_repo: HelmRepo, username: str | None = None, password: str | None = None, force_update: bool = False, **kwargs
) -> subprocess.CompletedProcess:
    """
    https://helm.sh/docs/helm/helm_repo_add/

    Args:
        helm_repo: helm repository definition
        username: chart repository username
        password: chart repository password
        force_update: replace (overwrite) the repo if it already exists
    """
    args = normalize_args(username=username, password=password, force_update=force_update)

    cp = subcommand_run(
        "add",
        helm_repo.name,
        str(helm_repo.url),
        *args,
        **kwargs,
    )
    return cp


def index(*args, **kwargs) -> subprocess.CompletedProcess:
    """
    https://helm.sh/docs/helm/helm_repo_index/
    """
    cp = subcommand_run("index", *args, **kwargs)
    return cp


def list(*args, **kwargs) -> List[HelmRepo]:
    """
    https://helm.sh/docs/helm/helm_repo_list/
    """
    data = subcommand_run("list", *args, "-o", "json", **kwargs).stdout
    return pydantic.parse_raw_as(List[HelmRepo], data or "[]")


def remove(*args, **kwargs) -> subprocess.CompletedProcess:
    """
    https://helm.sh/docs/helm/helm_repo_remove/
    """
    cp = subcommand_run("remove", *args, **kwargs)
    return cp


def update(*args, **kwargs) -> subprocess.CompletedProcess:
    """
    https://helm.sh/docs/helm/helm_repo_update/
    """
    cp = subcommand_run("update", *args, **kwargs)
    return cp
