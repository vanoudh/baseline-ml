import json
import urllib3


URL = "https://api.trumail.io/v2/lookups/json?email={}"


def check_email(email):
    url = URL.format(email)
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    js = json.loads(r.data)
    return js['deliverable']

