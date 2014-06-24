from urllib import request
from urllib.parse import urlencode, quote_plus

import simplejson


TINYSONG_KEY = ''
API_URL = 'http://tinysong.com/'


def init(key=''):
    if key:
        global TINYSONG_KEY
        TINYSONG_KEY = key


def api_call(query, method='a', format='json'):
    params = urlencode({'format': format, 'key': TINYSONG_KEY})
    url = API_URL + method + '/' + quote_plus(query) + '?' + params
    print(url)
    req = request.Request(url)
    response = request.urlopen(req).read()
    return simplejson.loads(response)
