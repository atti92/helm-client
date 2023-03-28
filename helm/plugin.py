from .common import helm_exec as helm_exec
from .common import kwargs_to_args


def exec(*args):
    return helm_exec("plugin", *args)


def install(*args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return exec("install", *args)


def list(*args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return exec("list", *args)


def uninstall(*args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return exec("uninstall", *args)


def update(*args, **kwargs):
    args = kwargs_to_args(*args, **kwargs)
    return exec("update", *args)
