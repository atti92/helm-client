from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import pydantic

from .common import helm_exec, kwargs_to_args
from .models import HelmRelease, HelmReleaseStatus


def env():
    """Get the helm client environment information"""
    return {
        line.split("=")[0]: line.split("=")[1].strip("'\"")
        for line in helm_exec("env").stdout.splitlines()
    }


def create(name: str, *args, starter: Optional[str | Path] = None, **kwargs):
    """This command creates a chart directory along with the common files and
    directories used in a chart.

    Args:
        name: Path to create the chart.
        starter: The name or absolute path to Helm starter scaffold.
    """
    args = kwargs_to_args(starter=starter, *args, **kwargs)
    return helm_exec("create", name, *args).stdout


def history(name: str, *args, max: Optional[int] = None, namespace: Optional[str] = None, **kwargs):
    """Get historical revisions for a given release.

    Args:
        name: Name of the release.
        max: A default maximum of 256 revisions will be returned. Setting this configures
            the maximum length of the revision list returned.
    """
    args = kwargs_to_args(*args, max=max, namespace=namespace, **kwargs)
    data = helm_exec("history", name, "-o", "json", *args)
    return pydantic.parse_raw_as(List[HelmRelease], data.stdout)


def install(name: str, chart: str, *args, namespace: Optional[str] = None, **kwargs):
    args = kwargs_to_args(*args, namespace=namespace, **kwargs)
    return helm_exec("install", name, chart, "-o", "json", *args)


def lint(path: str, *args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return helm_exec("lint", path, *args)


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
    args = kwargs_to_args(
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
    data = helm_exec("list", *args, "-o", "json", "--time-format", "2006-01-02T15:04:05")
    return pydantic.parse_raw_as(List[HelmRelease], data.stdout)


def package(path: str, *args, **kwargs):
    """This command packages a chart into a versioned chart archive file. If a path
    is given, this will look at that path for a chart (which must contain a
    Chart.yaml file) and then package that directory.
    """
    args = kwargs_to_args(*args, **kwargs)
    return helm_exec("package", path, *args)


def pull(chart: str, *args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return helm_exec("pull", chart, *args)


def push(chart, remote, *args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return helm_exec("push", chart, remote, *args)


def rollback(release: str, *args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return helm_exec("rollback", release, *args)


def status(release: str, *args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return helm_exec("status", release, *args)


def template(name, chart, *args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return helm_exec("template", name, chart, *args)


def test(release, *args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return helm_exec("test", release, *args)


def uninstall(release, *args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return helm_exec("uninstall", release, *args)


def upgrade(release, chart, *args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return helm_exec("upgrade", release, chart, *args)


def verify(path, *args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return helm_exec("verify", path, *args)


def version():
    """Get the helm client version information"""
    return helm_exec("version", "--short").stdout.strip()
