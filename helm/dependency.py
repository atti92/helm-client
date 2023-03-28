from .common import helm_exec as helm_exec
from .common import kwargs_to_args


def exec(*args):
    return helm_exec("dependency", *args)


def build(*args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return exec("build", *args)


def list(*args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return exec("list", *args)


def update(*args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return exec("update", *args)
