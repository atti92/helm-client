import subprocess

from pydantic import BaseModel, AnyUrl, HttpUrl

from helm.common import subprocess_run


class OciUrl(AnyUrl):
    allowed_schemes = {'oci'}

    __slots__ = ()


class HelmRepo(BaseModel):
    name: str
    url: HttpUrl | OciUrl

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


def add(
    helm_repo: HelmRepo,
    username: str | None = None,
    password: str | None = None,
    force_update: bool = False
) -> subprocess.CompletedProcess:
    """
    https://helm.sh/docs/helm/helm_repo_add/

    :param HelmRepo helm_repo: helm repository definition
    :param username: chart repository username
    :param password: chart repository password
    :param force_update: replace (overwrite) the repo if it already exists
    :return: CompletedProcess
    :rtype: subprocess.CompletedProcess
    """
    cmd = ["helm", "repo", "add", helm_repo.name, str(helm_repo.url)]
    if username is not None:
        cmd.extend(["--username", username])
    if password is not None:
        cmd.append("--password-stdin")
    if force_update:
        cmd.append("--force-update")

    cp = subprocess_run(cmd, input=password, check=True, text=True, capture_output=True)

    return cp

def update() -> subprocess.CompletedProcess:
    """
    https://helm.sh/docs/helm/helm_repo_update/

    :return: CompletedProcess
    :rtype: subprocess.CompletedProcess
    """""
    cmd = ["helm", "repo", "update"]

    cp = subprocess_run(cmd, check=True, text=True, capture_output=True)

    return cp
