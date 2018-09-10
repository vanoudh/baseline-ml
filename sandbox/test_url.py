
import json
import urllib3

email = "marc.vanoudheusden@gmail.co"
url = "https://api.trumail.io/v2/lookups/json?email={}".format(email)

http = urllib3.PoolManager()

r = http.request('GET', url)

js = json.loads(r.data)

# print(js)
print(js['deliverable'])

