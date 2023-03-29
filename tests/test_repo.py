from pydantic import HttpUrl

import helm
from helm.models import HelmRepo


def test_repo_add():
    cp = helm.repo.add(
        HelmRepo(name="bitnami", url=HttpUrl(url="https://charts.bitnami.com/bitnami", scheme="https")), dry_run=True
    )
    assert cp.args == ("helm", "repo", "add", "bitnami", "https://charts.bitnami.com/bitnami")


def test_repo_index():
    cp = helm.repo.index(dry_run=True)
    assert cp.args == ("helm", "repo", "index")


def test_repo_list():
    assert helm.repo.list(dry_run=True) == []


def test_repo_remove():
    cp = helm.repo.remove(dry_run=True)
    assert cp.args == ("helm", "repo", "remove")


def test_repo_update():
    cp = helm.repo.update(dry_run=True)
    assert cp.args == ("helm", "repo", "update")
