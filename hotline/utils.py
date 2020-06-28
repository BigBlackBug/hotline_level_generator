import functools
import os
import random
import string
from distutils.util import strtobool
from enum import Enum


def id_generator(size=8, chars=string.ascii_lowercase +
                               string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_raw_celery_task(task, bound=False):
    """
    Returns the pure function underneath celery task decorator
    for testing purposes
    :param task: celery task
    :param bound: True/False
    :return: function
    """
    return task.__wrapped__.__func__ if bound else task.__wrapped__


def extra_permissions(*classes):
    """
    Adds Extra Permissions to a view. Meant to be applied
    only to get/post/patch etc methods of view classes.
    :param classes: Permission Classes
    """

    def wrapper(func):
        @functools.wraps(func)
        def decorated_func(self, request, *args, **kwargs):
            old_permissions = self.permission_classes
            self.permission_classes = classes
            self.check_permissions(request)
            result = func(self, request, *args, **kwargs)
            self.permission_classes = old_permissions
            return result

        return decorated_func

    return wrapper


def _bool(value):
    return bool(strtobool(value))


def _str(value):
    return str(value)


class EnvType(Enum):
    BOOL = _bool
    STR = _str


def get_env(name, required=True, env_type=EnvType.STR):
    env = os.getenv(name)
    if required and not env:
        raise KeyError(f"{name} env is required")
    return env_type(env)
