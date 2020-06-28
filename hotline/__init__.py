import os
from distutils.util import strtobool
from enum import Enum

from .celery import app as celery_app

__all__ = ('celery_app',)


def _bool(value):
    return bool(strtobool(value))


class EnvType(Enum):
    BOOL = _bool
    STR = str


def get_env(name, required=True, env_type=EnvType.STR):
    env = os.getenv(name)
    if required and not env:
        raise KeyError(f"{name} env is required")
    return env_type(env)
