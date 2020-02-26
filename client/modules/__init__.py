from os.path import dirname, basename, isfile, join
import glob
import time
import trio

__all__ = ['load', 'memory', 'btcticker']

def interval(seconds=30):
    def decorator(function):
        async def wrapper(*args, **kwargs):
            await trio.sleep(seconds)
            return await function(*args, **kwargs)
        return wrapper
    return decorator
