import logging
import os
import platform
import re
import shutil
import stat
import subprocess
import tarfile
import zipfile
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)

# debug log strings
CP_DBG_CMD = "cmd: %s"
CP_DBG_OUT = "stdout: %s"
CP_DBG_ERR = "stderr: %s"


class Configuration:
    BIN_DIR = Path(__file__).parent / "bin"
    HELM_BINARY: str = "helm.exe" if platform.system().lower() == "windows" else "helm"
    HELM_PATH: Path = Path(HELM_BINARY)
    INSTALLED: Optional[bool] = None


def subprocess_run(
    *cmd: str, dry_run: bool = False, debug_stdout: bool = True, **kwargs
) -> subprocess.CompletedProcess:
    logger.debug(CP_DBG_CMD, cmd)

    if not dry_run:
        try:
            cp = subprocess.run(cmd, **kwargs)
        except subprocess.CalledProcessError as cpe:
            logger.error(CP_DBG_OUT, cpe.stdout)
            logger.error(CP_DBG_ERR, cpe.stderr)
            raise

        if debug_stdout:
            logger.debug(CP_DBG_OUT, cp.stdout)
        logger.debug(CP_DBG_ERR, cp.stderr)
    else:
        cp = subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")
    return cp


def helm_run(*args, dry_run: bool = False, debug_stdout: bool = True, **kwargs):
    return subprocess_run(
        str(Configuration.HELM_PATH),
        *args,
        dry_run=dry_run,
        debug_stdout=debug_stdout,
        check=True,
        text=True,
        capture_output=True,
        **kwargs,
    )


def normalize_args(*args, **kwargs):
    args = [item for item in args if item is not None]
    status = kwargs.pop("status", None)
    password = kwargs.pop("password", None)
    if password:
        kwargs["password-stdin"] = password
        kwargs["input"] = password
    if status:
        args.append(f"{status.value}")

    for key in kwargs.copy():
        if key in ("debug_stdout", "dry_run"):
            continue
        value = kwargs.pop(key)
        if not value:
            continue
        if len(key) == 1:
            args.append(f"-{key}")
        elif value is True:
            args.append(f"--{key}")
        else:
            args.extend([f"--{key}", value])
    return args


def ensure_installed():
    if Configuration.INSTALLED is None:
        check_installed()
    if Configuration.INSTALLED is True:
        return Configuration.HELM_PATH
    return install()


def install() -> Path:
    compressed_file_path = download_helm()
    return extract_helm(compressed_file_path)


def check_installed() -> Optional[str]:
    path = str(Configuration.BIN_DIR.absolute()) + os.pathsep + os.environ["PATH"]
    helm_path = shutil.which(Configuration.HELM_BINARY, path=path)
    if helm_path:
        Configuration.INSTALLED = True
        Configuration.HELM_PATH = Path(helm_path)
    else:
        Configuration.INSTALLED = False
    return helm_path


def get_latest_helm_version():
    release_page = requests.get("https://github.com/helm/helm/releases").content.decode()
    return next(re.finditer(r'href="/helm/helm/releases/tag/(v3.[0-9]*.[0-9]*)"', release_page)).group(1)


def get_helm_download_options():
    os = platform.system().lower()
    machine = platform.machine().lower()
    if "armv5" in machine:
        arch = "armv5"
    elif "armv6" in machine:
        arch = "armv6"
    elif "armv7" in machine:
        arch = "arm"
    elif "aarch64" in machine:
        arch = "arm64"
    elif "x86_64" in machine:
        arch = "amd64"
    elif "86" in machine:
        arch = "386"
    else:
        arch = machine
    ext = "zip" if os == "windows" else "tar.gz"
    return {"ext": ext, "os": os, "arch": arch}


def download_helm() -> Path:
    tag = get_latest_helm_version()
    options = get_helm_download_options()
    data = requests.get(f"https://get.helm.sh/helm-{tag}-{options['os']}-{options['arch']}.{options['ext']}")
    file_path = Configuration.BIN_DIR / f"helm.{options['ext']}"
    with file_path.open("wb") as fp:
        fp.write(data.content)
    return file_path


def extract_helm(file_path: Path):
    options = get_helm_download_options()
    if file_path.suffix == ".zip":
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            target = Configuration.BIN_DIR / Configuration.HELM_BINARY
            file_data = zip_ref.read(f"{options['os']}-{options['arch']}/{Configuration.HELM_BINARY}")
    else:
        with tarfile.open(file_path, "r:gz") as tar_ref:
            target = Configuration.BIN_DIR / Configuration.HELM_BINARY
            file_data = tar_ref.extractfile(
                f"{options['os']}-{options['arch']}/{Configuration.HELM_BINARY}").read()  # type: ignore

    target.write_bytes(file_data)
    os.chmod(target, os.stat(target).st_mode | stat.S_IEXEC)
    check_installed()
    return target
