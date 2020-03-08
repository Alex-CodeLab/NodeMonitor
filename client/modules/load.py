import os
import json
from . import interval


@interval(1)
async def load():
    avg_1, avg_5, avg_10 = list(map(str, os.popen('uptime')))[
        0].split(':')[-1].strip().split(', ')
    value = avg_1.replace(',', '.')
    msg = {"module": "load", "value": value}
    return json.dumps(msg)
