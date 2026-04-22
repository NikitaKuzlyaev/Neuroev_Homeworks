from functools import wraps

from framework.context import Context


def context_storage(name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            Context.add(name, result)
            return result

        return wrapper

    return decorator
