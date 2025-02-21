
```python
from flask import Flask, request
import jwt, time, os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

private_key = open('priv').read()
public_key = open('pub').read()
flag = open('flag.txt').read()

@app.route("/get_token")
def get_token():
    return jwt.encode({'admin': False, 'now': time.time()}, private_key, algorithm='RS256')

@app.route("/get_flag", methods=['POST'])
def get_flag():
  try:
    payload = jwt.decode(request.form['jwt'], public_key, algorithms=['RS256'])
    if payload['admin']:
      return flag
  except:
    return ":("

@app.route("/")
def sauce():
  return "%s" % open(__file__).read()

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
```

We can obtain the public key from **two** separately-generated JWTs with `https://github.com/silentsignal/rsa_sign2n`

```bash
python3 jwt_forgery.py eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhZG1pbiI6ZmFsc2UsIm5vdyI6MTYzMjUzNjcyMC41NjkyMTk4fQ.DGGgcbIX160FUcUr6JWLn8HLGQM3n_DuIQ0tDx0AcTKXr_72_Z6LdMFo33yScKiobGFpjzlAg6lDMsCa4UkJqQfteA38Mo74B7ITHpjh0tnXrxejm20F-X23kTkKT_SLVw eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhZG1pbiI6ZmFsc2UsIm5vdyI6MTYzMjUzNjc0MS40NDAyMzA0fQ.DxCSrEVez5gtm_Xfjq1eaiGRf5PKNeYXti3loMHYMURKQdjILlp1dZlCSed1Y4R1B9mOsbAujxOYCLsdjQhzIbLV04XHZ96UOXH0dXaqNTb_PBxCsZ5ELs_CFX6qNm9MJA

[*] GCD:  0x1d
[*] GCD:  0x108b7c75aee1e2b9df3692a2cc54b100d111002193ebc9c3cf575e4b16f595cc28d9b47a65d1f3774aa3db05649085589230fe23bfcc2ef876b4134dafde4484d7bde8c9b80016d9c9aed53a0334ae3483cc833374301e1a7829a5f5800a793803
[+] Found n with multiplier 1  :
 0x108b7c75aee1e2b9df3692a2cc54b100d111002193ebc9c3cf575e4b16f595cc28d9b47a65d1f3774aa3db05649085589230fe23bfcc2ef876b4134dafde4484d7bde8c9b80016d9c9aed53a0334ae3483cc833374301e1a7829a5f5800a793803
[+] Written to 108b7c75aee1e2b9_65537_x509.pem
[+] Tampered JWT: b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6IGZhbHNlLCAibm93IjogMTYzMjUzNjcyMC41NjkyMTk4LCAiZXhwIjogMTYzMjYyMzE5OX0._rQf-v9lQvZInV6MBEjkBqzuEcPtx-gaobU0oHtjpHY'
[+] Written to 108b7c75aee1e2b9_65537_pkcs1.pem
[+] Tampered JWT: b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6IGZhbHNlLCAibm93IjogMTYzMjUzNjcyMC41NjkyMTk4LCAiZXhwIjogMTYzMjYyMzE5OX0.-xQ_LSF9jJaAEdd2PCgPZjZVwlX8wAD4H2P7lTZOw84'
[+] Found n with multiplier 29  :
 0x920d1e8a71b85eaf6bd01744d6c84f79f7c2361f955f3bb7b3907e2cedfc567cfeadf290c09e76df43717bc5acb5265d51233f069d1c1a390f097e43db86c6c9a571f54cf72ced06f45fa0e5a0b68f0d5f53f8f259ef620424bf1a1ee5e0de9f
[+] Written to 920d1e8a71b85eaf_65537_x509.pem
[+] Tampered JWT: b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6IGZhbHNlLCAibm93IjogMTYzMjUzNjcyMC41NjkyMTk4LCAiZXhwIjogMTYzMjYyMzE5OX0.V1XnPFpwKbK3IuFNChLZU0XkvMUyzjIKwSVQEyjIqIs'
[+] Written to 920d1e8a71b85eaf_65537_pkcs1.pem
[+] Tampered JWT: b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6IGZhbHNlLCAibm93IjogMTYzMjUzNjcyMC41NjkyMTk4LCAiZXhwIjogMTYzMjYyMzE5OX0.a1fUyscIftGuetBSD1OnIKKY8p-DjMB6sIMJibWpnpM'
================================================================================
Here are your JWT's once again for your copypasting pleasure
================================================================================
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6IGZhbHNlLCAibm93IjogMTYzMjUzNjcyMC41NjkyMTk4LCAiZXhwIjogMTYzMjYyMzE5OX0._rQf-v9lQvZInV6MBEjkBqzuEcPtx-gaobU0oHtjpHY
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6IGZhbHNlLCAibm93IjogMTYzMjUzNjcyMC41NjkyMTk4LCAiZXhwIjogMTYzMjYyMzE5OX0.-xQ_LSF9jJaAEdd2PCgPZjZVwlX8wAD4H2P7lTZOw84
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6IGZhbHNlLCAibm93IjogMTYzMjUzNjcyMC41NjkyMTk4LCAiZXhwIjogMTYzMjYyMzE5OX0.V1XnPFpwKbK3IuFNChLZU0XkvMUyzjIKwSVQEyjIqIs
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6IGZhbHNlLCAibm93IjogMTYzMjUzNjcyMC41NjkyMTk4LCAiZXhwIjogMTYzMjYyMzE5OX0.a1fUyscIftGuetBSD1OnIKKY8p-DjMB6sIMJibWpnpM
```

We can ignore all the output and focus on these two lines:

```
[+] Written to 108b7c75aee1e2b9_65537_x509.pem
[+] Written to 920d1e8a71b85eaf_65537_x509.pem
```

These are the TWO possible public keys that it generated from the tokens we gave it.

From experience, this is probabilistic. At first I tried two **different** tokens and it generated SIX possible public keys. I didn't want to try all of those so I just generated two new tokens and re-ran it. I got lucky then in that it generated only TWO.

Let's see what the first public key looks like:

```pem
# cat 108b7c75aee1e2b9_65537_x509.pem
-----BEGIN PUBLIC KEY-----
MHwwDQYJKoZIhvcNAQEBBQADawAwaAJhEIt8da7h4rnfNpKizFSxANERACGT68nD
z1deSxb1lcwo2bR6ZdHzd0qj2wVkkIVYkjD+I7/MLvh2tBNNr95EhNe96Mm4ABbZ
ya7VOgM0rjSDzIMzdDAeGngppfWACnk4AwIDAQAB
-----END PUBLIC KEY-----
```

Now that we have a public key, let's use the other special tool to see if we can generate a private key from it (which is only possible if it is a "weak" public key).

`https://github.com/Ganapati/RsaCtfTool`

```bash
python3 RsaCtfTool.py --publickey ./public.key --private

[*] Testing key ./public.key.
[*] Performing pastctfprimes attack on ./public.key.
\297337.74it/s]
[*] Performing system_primes_gcd attack on ./public.key.
  0%|▍                                                                                                                                            | 21/7007 [00:00<00:08, 789.12it/s]
[*] Attack success with system_primes_gcd method !

Results for ./public.key:

Private key :
-----BEGIN RSA PRIVATE KEY-----
MIIB+wIBAAJhEIt8da7h4rnfNpKizFSxANERACGT68nDz1deSxb1lcwo2bR6ZdHz
d0qj2wVkkIVYkjD+I7/MLvh2tBNNr95EhNe96Mm4ABbZya7VOgM0rjSDzIMzdDAe
GngppfWACnk4AwIDAQABAmEKpfUIG6wBMAOtnv0vdki0XiDfW6KTMDRDvdcjryUd
sIi8WaAV8ZW9z9XWw/v8U/4DrOzW5nJwm2BwMRfpIfKlS/QW0gX/TR+btntJc6P8
wnks0vynK8S9A+l4kegxYrSxAmEAkg0einG4Xq9r0BdE1shPeffCNh+VXzu3s5B+
LO38Vnz+rfKQwJ5230Nxe8WstSZdUSM/Bp0cGjkPCX5D24bGyaVx9Uz3LO0G9F+g
5aC2jw1fU/jyWe9iBCS/Gh7l4N6fAgEdAmBhCOJfrQqHrhj9WlhcMx3KtTeNahJ+
AVkdrkSGaV+bvtQekehmcWIdF9wQFdeXS3P4cmhvZnbDXWGGNyOyeKseUhOSnJ4k
dR6HwflOVyaziHjre5zY79i5VAi7vAeTDZUCAQUCYG7MKNL1KsNqmGjlg6vEGPts
ga15EDaXO+lTIe0eeM7aaO3kJzEFdKlfTUNp0nfE1AiWUx+AA6n2UgczpjybNbN0
rroXE8nOS+WGVr/bBhQ/HC4MTevzZNcBZNYFyN+OZw==
-----END RSA PRIVATE KEY-----
```

# Solution

```python
import jwt

private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIB+wIBAAJhEIt8da7h4rnfNpKizFSxANERACGT68nDz1deSxb1lcwo2bR6ZdHz
d0qj2wVkkIVYkjD+I7/MLvh2tBNNr95EhNe96Mm4ABbZya7VOgM0rjSDzIMzdDAe
GngppfWACnk4AwIDAQABAmEKpfUIG6wBMAOtnv0vdki0XiDfW6KTMDRDvdcjryUd
sIi8WaAV8ZW9z9XWw/v8U/4DrOzW5nJwm2BwMRfpIfKlS/QW0gX/TR+btntJc6P8
wnks0vynK8S9A+l4kegxYrSxAmEAkg0einG4Xq9r0BdE1shPeffCNh+VXzu3s5B+
LO38Vnz+rfKQwJ5230Nxe8WstSZdUSM/Bp0cGjkPCX5D24bGyaVx9Uz3LO0G9F+g
5aC2jw1fU/jyWe9iBCS/Gh7l4N6fAgEdAmBhCOJfrQqHrhj9WlhcMx3KtTeNahJ+
AVkdrkSGaV+bvtQekehmcWIdF9wQFdeXS3P4cmhvZnbDXWGGNyOyeKseUhOSnJ4k
dR6HwflOVyaziHjre5zY79i5VAi7vAeTDZUCAQUCYG7MKNL1KsNqmGjlg6vEGPts
ga15EDaXO+lTIe0eeM7aaO3kJzEFdKlfTUNp0nfE1AiWUx+AA6n2UgczpjybNbN0
rroXE8nOS+WGVr/bBhQ/HC4MTevzZNcBZNYFyN+OZw==
-----END RSA PRIVATE KEY-----"""

token = jwt.encode({'admin': True, 'now': 1632536761.4651732}, private_key, algorithm='RS256')
print(token)
```