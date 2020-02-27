import json
import requests
from . import interval

@interval(10)
async def btcticker():
    response = requests.get('https://blockchain.info/ticker')
    res = response.json()
    return 'btcticker ' + json.dumps({"value": str(res["USD"]["15m"])})
