#!/usr/bin/python

from urllib.parse import urlencode
import urllib.request
import json

token = '7d1fc460f507013114b94e6a4037cf04'

requestParams = {
    "token": token,
    "per_page": 100
}

base_url = "https://api.groupme.com/v3/groups?"

request_url = base_url + urlencode(requestParams)

print(request_url)

response = urllib.request.urlopen(request_url)
data = json.loads(response.read().decode("utf-8"))

print("{} TOTAL GROUPS".format(len(data['response'])))

for entry in data['response']:
    print(entry['id'] + ': ' + entry['name'])
