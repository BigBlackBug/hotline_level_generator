import functools
import random
import string


def id_generator(size=8, chars=string.ascii_lowercase +
                               string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_celery_task(task, bound):
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
