from functools import wraps
from random import random
from time import sleep

from got_search.utils.typevars import A


def identity(x: A) -> A:
    return x

def delay(*, min_sleep=1, duration=1):
    """Decorator to delay execution of a function by a random duration
    """

    def dec(f):
        @wraps(f)
        def f_with_delay(*args, **kwargs):
            print(
                f'Delaying between {min_sleep} and {min_sleep + duration} seconds...')
            sleep(min_sleep + random() * duration)
            return f(*args, **kwargs)

        return f_with_delay

    return dec
