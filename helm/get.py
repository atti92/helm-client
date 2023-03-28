from .common import helm_exec as helm_exec
from .common import kwargs_to_args


def exec(*args):
    return helm_exec("get", *args)


def all(*args, **kwargs):
    """download all information for a named release"""
    args = kwargs_to_args(*args, **kwargs)
    return exec("all", *args)


def hooks(*args, **kwargs):
    """download all hooks for a named release"""
    args = kwargs_to_args(*args, **kwargs)
    return exec("hooks", *args)


def manifest(*args, **kwargs):
    """download the manifest for a named release"""
    args = kwargs_to_args(*args, **kwargs)
    return exec("manifest", *args)


def notes(*args, **kwargs):
    """download the notes for a named release"""
    args = kwargs_to_args(*args, **kwargs)
    return exec("notes", *args)


def values(*args, **kwargs):
    """download the values file for a named release"""
    args = kwargs_to_args(*args, **kwargs)
    return exec("values", *args)
