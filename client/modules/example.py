import json
from . import interval

from random import randint

@interval(5)
async def example():
    value = randomint(0,100)
    msg = {"module": "example", "value": value}
    return json.dumps(msg)
