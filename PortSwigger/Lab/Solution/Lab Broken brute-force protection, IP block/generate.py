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