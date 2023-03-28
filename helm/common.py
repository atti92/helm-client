import subprocess

from .models import ProcessReturn


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
