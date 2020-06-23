
def get_celery_task(task, bound):
    """
    Returns the pure function underneath celery task decorator
    for testing purposes
    :param task: celery task
    :param bound: True/False
    :return: function
    """
    return task.__wrapped__.__func__ if bound else task.__wrapped__
