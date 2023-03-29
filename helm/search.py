from typing import List, Optional

import pydantic

from helm.common import helm_run, normalize_args
from helm.models import HelmChartInfo


def subcommand_run(*args, **kwargs):
    return helm_run("search", *args, **kwargs)


def hub(*args, **kwargs) -> List[HelmChartInfo]:
    """https://helm.sh/docs/helm/helm_search_hub/"""
    args = normalize_args(*args, **kwargs)
    data = subcommand_run("hub", *args, "-o", "json", **kwargs).stdout
    return pydantic.parse_raw_as(List[HelmChartInfo], data or "[]")


def repo(keyword: Optional[str] = None, *args, **kwargs) -> List[HelmChartInfo]:
    """https://helm.sh/docs/helm/helm_search_repo"""
    args = normalize_args(keyword, *args, **kwargs)
    data = subcommand_run("repo", *args, "-o", "json", **kwargs).stdout
    return pydantic.parse_raw_as(List[HelmChartInfo], data or "[]")
