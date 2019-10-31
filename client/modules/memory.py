import os
import json
from . import interval

@interval(5)
def memory():
    tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    return 'memory' + json.dumps({"total":tot_m, "used": used_m, "free": free_m})
