import logging
import subprocess

logger = logging.getLogger(__name__)

# debug log strings
CP_DBG_CMD = "cmd: %s"
CP_DBG_OUT = "stdout: %s"
CP_DBG_ERR = "stderr: %s"


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
        "helm", *args, dry_run=dry_run, debug_stdout=debug_stdout, check=True, text=True, capture_output=True, **kwargs
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
