#!/usr/bin/env python

# https://stackoverflow.com/questions/16337511/log-all-requests-from-the-python-requests-module/16337639#16337639

import requests
import logging
logging.basicConfig(level=logging.DEBUG)
r = requests.get('http://httpbin.org/get?foo=bar&baz=python')
