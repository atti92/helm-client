import yaml

from helm.common import helm_run, normalize_args
from helm.models import HelmChartInfo


def subcommand_run(*args, **kwargs):
    return helm_run("show", *args, **kwargs)


def all(*args, **kwargs):
    args = normalize_args(*args, **kwargs)
    return subcommand_run("all", *args, **kwargs)


def chart(chart: str | HelmChartInfo, *args, **kwargs) -> dict:
    if isinstance(chart, HelmChartInfo):
        chart = chart.name
    args = normalize_args(*args, **kwargs)
    data = subcommand_run("chart", chart, *args, **kwargs).stdout
    return yaml.safe_load(data)


def crds(chart: str | HelmChartInfo, *args, **kwargs):
    if isinstance(chart, HelmChartInfo):
        chart = chart.name
    args = normalize_args(*args, **kwargs)
    return subcommand_run("crds", *args, **kwargs)


def readme(chart: str | HelmChartInfo, *args, **kwargs) -> str:
    if isinstance(chart, HelmChartInfo):
        chart = chart.name
    args = normalize_args(*args, **kwargs)
    return subcommand_run("readme", *args, **kwargs).stdout


def values(chart: str | HelmChartInfo, *args, **kwargs) -> dict:
    if isinstance(chart, HelmChartInfo):
        chart = chart.name
    args = normalize_args(*args, **kwargs)
    data = subcommand_run("values", *args, **kwargs).stdout
    return yaml.safe_load(data)
