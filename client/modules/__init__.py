from os.path import dirname, basename, isfile, join
import glob
import time

def interval(seconds=30):
    def decorator(function):
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            return function(*args, **kwargs)
        return wrapper
    return decorator
