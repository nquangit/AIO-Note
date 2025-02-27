# Write up csc.tf

## Web

### Feature Unlocked

Command Injection

![image](https://hackmd.io/_uploads/H1GSzmlnA.png)

![image](https://hackmd.io/_uploads/rJjDzml3A.png)

Run a validation server with modifided code from the source code. Then goto `/release?debug=true` and modify the `preferences` cookie (add the `validation_server` with your own server's address)

![image](https://hackmd.io/_uploads/HkLFGmenA.png)

Flag: `CSCTF{d1d_y0u_71m3_7r4v3l_f0r_7h15_fl46?!}`


### Trendz

LFI to read the JWT secret key and IDOR to read other user post

![image](https://hackmd.io/_uploads/SJfmbvghC.png)


`GET /static.%2E/jwt.secret`

Modify the original `JWTAuth.go` file to sign your token with custom data and secret key. Note: **Remember to set the `JWT_SECRET_KEY` environment variable and create `jwt.secret` file.**

`Fun: I got stuck on the jwt.secret file for what felt like forever, all because I used Windows to create it. And oh boy, did I pay the price... cursed by the evil forces of CRLF! 😂`

![image](https://hackmd.io/_uploads/rkqSSIlhR.png)

![image](https://hackmd.io/_uploads/rJ3xVLe2C.png)

Get the accesstoken then goto `/admin/dashboard`. We the a hidden post with post id. Access the post with `/user/posts/<post_id>`.


### Trendzz

Race condition

`CSCTF{d2426fb5-a93a-4cf2-b353-eac8e0e9cf94}`

![image](https://hackmd.io/_uploads/H17FkvxhA.png)


### Trendzzz

![image](https://hackmd.io/_uploads/rJ3xVLe2C.png)

![image](https://hackmd.io/_uploads/rkqSSIlhR.png)

![image](https://hackmd.io/_uploads/BkusUIl30.png)

Get the accesstoken and the refreshtoken then goto `/superadmin/dashboard`
