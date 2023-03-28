import subprocess
import logging
from .models import ProcessReturn

logger = logging.getLogger(__name__)

# debug log strings
CP_DBG_CMD = 'cmd: %s'
CP_DBG_OUT = 'stdout: %s'
CP_DBG_ERR = 'stderr: %s'


def helm_exec(command, *args, timeout=None) -> ProcessReturn:
    proc = subprocess.Popen(
        ["helm", command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate(timeout=timeout)
    return ProcessReturn(stdout=stdout.decode(), stderr=stderr.decode(), returncode=proc.returncode)


def kwargs_to_args(*args, **kwargs):
    args = list(args)
    status = kwargs.pop("status")

    if status:
        args.append(f"{status.value}")

    for key, value in kwargs.items():
        if not value:
            continue
        if len(key) == 1:
            args.append(f"-{key}")
        elif value is True:
            args.append(f"--{key}")
        else:
            args.extend([f"--{key}", value])
    return args


def subprocess_run(
    cmd: list[str],
    dryrun: bool = False,
    debug_stdout: bool = True,
    **kwargs
) -> subprocess.CompletedProcess:
    logger.debug(CP_DBG_CMD, cmd)

    if not dryrun:
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
        cp = subprocess.CompletedProcess(args=cmd, returncode=0, stdout='', stderr='')

    return cp
