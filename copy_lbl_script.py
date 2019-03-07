#!/usr/bin/python3.5

import requests
import json
import sys

if len(sys.argv) < 2:
    print ("Usage: script.py github_token")
    sys.exit(-1)

TOKEN = sys.argv[1]
url_source = "https://api.github.com/repos/Toxa-man/labWorks_8373_2018/labels"
url_dest = "https://api.github.com/repos/Toxa-man/labWorks_8373_2019/labels"

for obj in requests.get(url_dest).json():
    requests.delete(url_dest + "/" + obj["name"], headers={'Authorization': 'token %s' % TOKEN})

for obj in requests.get(url_source).json():
    requests.post(url_dest, json={"name" : obj["name"], "description" : "", "color" : obj["color"]}, headers={'Authorization': 'token %s' % TOKEN})



