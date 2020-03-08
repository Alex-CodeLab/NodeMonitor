import os
import json
from . import interval

@interval(2)
async def memory():
    tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    data = {"total":tot_m, "used": used_m, "value": free_m }
    msg = {"module": "memory", "data": data}
    return json.dumps(msg)
