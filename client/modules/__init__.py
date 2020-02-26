from os.path import dirname, basename, isfile, join
import glob
import time
import trio

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

def interval(seconds=30):
    def decorator(function):
        async def wrapper(*args, **kwargs):
            await trio.sleep(seconds)
            return await function(*args, **kwargs)
        return wrapper
    return decorator
