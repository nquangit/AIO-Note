# Lab: High-level logic vulnerability

This lab is only check for the total price on the order.

Buy [Lightweight "l33t" Leather Jacket](https://0aa300750462587cd756782d007400db.web-security-academy.net/product?productId=1) with quantity `1` then buy something with quantity `-x` to balance the price to be sure that the total price is greater than 0.

# Lab: Inconsistent security controls

This lab is missing check/verify email domain on the change email function. Then we can login as the normal user then change the mail to the [dontwannacry.com](file://./workspace/aecd0b61-f20e-4d5d-9a85-e3fbba8eeb59/dontwannacry.com) to login as Admin.

# Lab: Flawed enforcement of business rules

This lab check coupon doesn't reuse by by COMPARE WITH THE LAST COUPON, we got 2 coupon code from this site, so use it interleaved, one by one util enough to buy.

# Lab: Inconsistent handling of exceptional input

This lab will truncated the email address if it is too long (maximum 255 character) then we can inject a long address like:

```
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@dontwannacry.com.exploit-0a0400b604f4210b80611b0701e20004.exploit-server.net
```

Then it will become

```
aaaa..aaa@dontwannacry.com
```

# Lab: Weak isolation on dual-use endpoint

On this lab, in the change password function, it uses both for update Administrator password(without current password) and update User password (with current password). And the username passed to the body POST body.

Then we can use this function to update password for Administrator account by only pass the `username`

# Lab: Insufficient workflow validation

On this lab, when we make a Place Order, it will check for the **Store credit** then it will redirect to `/cart/order-confirmation?order-confirmed=true` and Complete the order. But in the order confirmation it not check/verify the order, it's all rely the GET parameter `order-confirmed`. Then we just add our product we wanna buy and go to the path `/cart/order-confirmation` with `order-confirmed=true`.

# Lab: Authentication bypass via flawed state machine

On this lab, on the Role Selector page after the login page, if we drop the GET method to this page and go directly to the `/admin`then we can bypass the access.

# Lab: Infinite money logic flaw

In this lab, we can buy a gift card with $10 price and it's value is also $10, but on the checkout we can use the COUPON code (infinite/forever) to buy a gift card with only $7, then we apply this gift card, we got $10.

With a gift card we can got $3, so buy 1 and apply 1, we will increse the credit store infinite money.

# Lab: Authentication bypass via encryption oracle

In this lab, on the stay log in cookie, it was encrypted but it use the same encrypt/decrypt method for the notification function. So we can use the notification to decrypt and verify the encrypt.

Put the encrypted stay-log-in cookie in the notification and we got the plaintext `username:timestamp` Enter an invalid email address (administrator:timestamp) on the Update email or Comment function and then we got the cipher text for `Invalid email address: <invalid_email>`. The notification cookie was encrypted and encoded, extract by URL decode -> Base64 decode -> Hex then we can try to remove first 23 bytes (for the string: `Invalid email address: `). Then encode it, but we got an Internal Server Error with message like: The input must be divided by 16 byes. Then add padding to the <invalid_email> for complete the input length 32-23=9bytes

The final email like: `zzzzzzzzzadministrator:1735199645105` Decode it to hex, and remove the first 32 bytes - Remaining 32 bytes (remove 32 bytes include "Invalid email address: " and the padding we just added)

Then we got the cipher for `administrator:1735199645105`Check it by add it to the notification cookie.


# Lab: Bypassing access controls using email address parsing discrepancies

https://portswigger.net/research/splitting-the-email-atom#unicode-overflows

Using the UTF-7 encoding to bypass.

```
// HTTP Request Body
csrf=Xdt3nEFMKBBxaqZrsXVQ8JkWy8hjRL99&username=n&email=%3D%3Futf-7%3Fq%3Fattacker%26AEA-exploit-0a9a003404777ac1844121b70108001c.exploit-server.net%26ACA-%3F%3D%40ginandjuice.shop&password=n

-> Email: =?utf-7?q?attacker&AEA-[YOUR-EXPLOIT-SERVER_ID]&ACA-?=@ginandjuice.shop.
```

We can use CyberChef to encode email to UTF-7 but we need to change the prefix from `+` to `&`. Ex: `@` -> `+AEA` -> `&AEA`

