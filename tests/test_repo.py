from pydantic import HttpUrl

from helm import repo
from helm.repo import HelmRepo


def test_repo_update_dryrun():
    repo.add(HelmRepo(
        name="bitnami",
        url=HttpUrl(url='https://charts.bitnami.com/bitnami', scheme='https')
    ))
    repo.update()
