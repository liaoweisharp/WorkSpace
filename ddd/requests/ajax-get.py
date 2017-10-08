import traceback
import urllib

import requests

_url = 'http://www.xiami.com/count/getplaycount'

data = {'id': 2739, 'type': 'artist'}

data = urllib.urlencode(data)

url = _url + '?' + data
try:
    r = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
    print r.text
except:
    traceback.print_exc()
