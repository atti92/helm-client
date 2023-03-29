from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import pydantic

from .common import helm_run, normalize_args
from .models import HelmRelease, HelmReleaseStatus


def env(**kwargs):
    """Get the helm client environment information"""
    return {
        line.split("=")[0]: line.split("=")[1].strip("'\"") for line in helm_run("env", **kwargs).stdout.splitlines()
    }


def create(name: str, *args, starter: Optional[str | Path] = None, **kwargs):
    """This command creates a chart directory along with the common files and
    directories used in a chart.

    Args:
        name: Path to create the chart.
        starter: The name or absolute path to Helm starter scaffold.
    """
    args = normalize_args(starter=starter, *args, **kwargs)
    return helm_run("create", name, *args, **kwargs).stdout


def history(name: str, *args, max: Optional[int] = None, namespace: Optional[str] = None, **kwargs):
    """Get historical revisions for a given release.

    Args:
        name: Name of the release.
        max: A default maximum of 256 revisions will be returned. Setting this configures
            the maximum length of the revision list returned.
    """
    args = normalize_args(*args, max=max, namespace=namespace, **kwargs)
    data = helm_run("history", name, "-o", "json", *args, **kwargs)
    return pydantic.parse_raw_as(List[HelmRelease], data.stdout)


def install(name: str, chart: str, *args, namespace: Optional[str] = None, **kwargs):
    args = normalize_args(*args, namespace=namespace, **kwargs)
    return helm_run("install", name, chart, "-o", "json", *args, **kwargs)


def lint(path: str, *args, **kwargs):
    args = normalize_args(*args, **kwargs)
    return helm_run("lint", path, *args, **kwargs)


def list(
    *args,
    status: Optional[HelmReleaseStatus] = None,
    all_namespaces: bool = False,
    filter_string: Optional[str] = None,
    max: Optional[int] = None,
    reverse: bool = False,
    selector: Optional[str] = None,
    namespace: Optional[str] = None,
    **kwargs,
) -> List[HelmRelease]:
    """This command lists all of the releases for a specified namespace.

    Args:
        status: Filter on release status.
        all_namespaces: list releases across all namespaces.
        filter_string: a regular expression (Perl compatible).
            Any releases that match the expression will be included in the results.
        max: maximum number of releases to fetch (default 256).
        reverse: reverse the sort order.
        selector: Selector (label query) to filter on,
            supports '=', '==', and '!='.(e.g. -l key1=value1,key2=value2).
            Works only for secret(default) and configmap storage backends.
    """
    args = normalize_args(
        *args,
        namespace=namespace,
        status=status,
        all_namespaces=all_namespaces,
        filter_string=filter_string,
        max=max,
        reverse=reverse,
        selector=selector,
        **kwargs,
    )
    data = helm_run("list", *args, "-o", "json", "--time-format", "2006-01-02T15:04:05")
    return pydantic.parse_raw_as(List[HelmRelease], data.stdout, **kwargs)


def package(path: str, *args, **kwargs):
    """This command packages a chart into a versioned chart archive file. If a path
    is given, this will look at that path for a chart (which must contain a
    Chart.yaml file) and then package that directory.
    """
    args = normalize_args(*args, **kwargs)
    return helm_run("package", path, *args, **kwargs)


def pull(chart: str, *args, **kwargs):
    args = normalize_args(*args, **kwargs)
    return helm_run("pull", chart, *args, **kwargs)


def push(chart, remote, *args, **kwargs):
    args = normalize_args(*args, **kwargs)
    return helm_run("push", chart, remote, *args, **kwargs)


def rollback(release: str, *args, **kwargs):
    args = normalize_args(*args, **kwargs)
    return helm_run("rollback", release, *args, **kwargs)


def status(release: str, *args, **kwargs):
    args = normalize_args(*args, **kwargs)
    return helm_run("status", release, *args, **kwargs)


def template(name, chart, *args, **kwargs):
    args = normalize_args(*args, **kwargs)
    return helm_run("template", name, chart, *args, **kwargs)


def test(release, *args, **kwargs):
    args = normalize_args(*args, **kwargs)
    return helm_run("test", release, *args, **kwargs)


def uninstall(release, *args, **kwargs):
    args = normalize_args(*args, **kwargs)
    return helm_run("uninstall", release, *args, **kwargs)


def upgrade(release, chart, *args, **kwargs):
    args = normalize_args(*args, **kwargs)
    return helm_run("upgrade", release, chart, *args, **kwargs)


def verify(path, *args, **kwargs):
    args = normalize_args(*args, **kwargs)
    return helm_run("verify", path, *args, **kwargs)


def version(**kwargs):
    """Get the helm client version information"""
    return helm_run("version", "--short", **kwargs).stdout.strip()
