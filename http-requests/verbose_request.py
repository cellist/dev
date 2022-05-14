#!/usr/bin/env python

# https://stackoverflow.com/questions/16337511/log-all-requests-from-the-python-requests-module/16337639#16337639

import requests
import logging
from http.client import HTTPConnection  # py3

log = logging.getLogger('urllib3')
log.setLevel(logging.DEBUG)

# logging from urllib3 to console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

# print statements from `http.client.HTTPConnection` to console/stdout
HTTPConnection.debuglevel = 1

requests.get('http://httpbin.org/get?foo=bar&baz=python')
