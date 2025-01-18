In this section, we'll explain HTTP request smuggling attacks and describe how common request smuggling vulnerabilities can arise.

**MUST READ**

```
CL.TE: Content-Length.Transfer-Encoding

Extension: HTTP Request Smuggler

Todo:

1. Send the request to the BurpSuite Repeater
2. Change the request method from GET to POST (if not)
3. Convert to chunked (use HTTP Request Smuggler Extension)
4. Change to use the HTTP/1.1

With CL.TE
- Not turn off Auto update Content-Length
- Add the next request below original request (with 2 or 3 empty line)
- Without 2 new line (\r\n\r\n) at the end
- Remove chunk if exist (only data)

With TE.CL
- Turn off Auto update Content-Length
- We can use the extension above to auto generate the chunked
- Chunk start with a size (in hex) follow by \r\n then the body
(multiple link) and the finally is 0 (with \r\n\r\n)

Obfuscating the TE by add multiple TE header. (Check the lab)
```

## What is HTTP request smuggling?

HTTP request smuggling is a technique for interfering with the way a web site processes sequences of HTTP requests that are received from one or more users. Request smuggling vulnerabilities are often critical in nature, allowing an attacker to bypass security controls, gain unauthorized access to sensitive data, and directly compromise other application users.

Request smuggling is primarily associated with HTTP/1 requests. However, websites that support HTTP/2 may be vulnerable, depending on their back-end architecture.

#### PortSwigger Research

HTTP request smuggling was first documented in 2005, and repopularized by PortSwigger's extensive research on the topic. For details, check out the following whitepapers:

- [HTTP desync attacks: Request smuggling reborn](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn)
- [HTTP/2: The sequel is always worse](https://portswigger.net/research/http2)
- [Browser-powered desync attacks: A new frontier in HTTP request smuggling](https://portswigger.net/research/browser-powered-desync-attacks)

## What happens in an HTTP request smuggling attack?

Today's web applications frequently employ chains of HTTP servers between users and the ultimate application logic. Users send requests to a front-end server (sometimes called a load balancer or reverse proxy) and this server forwards requests to one or more back-end servers. This type of architecture is increasingly common, and in some cases unavoidable, in modern cloud-based applications.

When the front-end server forwards HTTP requests to a back-end server, it typically sends several requests over the same back-end network connection, because this is much more efficient and performant. The protocol is very simple; HTTP requests are sent one after another, and the receiving server has to determine where one request ends and the next one begins:

In this situation, it is crucial that the front-end and back-end systems agree about the boundaries between requests. Otherwise, an attacker might be able to send an ambiguous request that gets interpreted differently by the front-end and back-end systems:

Here, the attacker causes part of their front-end request to be interpreted by the back-end server as the start of the next request. It is effectively prepended to the next request, and so can interfere with the way the application processes that request. This is a request smuggling attack, and it can have devastating results.

## How do HTTP request smuggling vulnerabilities arise?

Most HTTP request smuggling vulnerabilities arise because the HTTP/1 specification provides two different ways to specify where a request ends: the`Content-Length`header and the`Transfer-Encoding`header.

The`Content-Length`header is straightforward: it specifies the length of the message body in bytes. For example:

```HTTP
POST /search HTTP/1.1
Host: normal-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 11

q=smuggling
```

The`Transfer-Encoding`header can be used to specify that the message body uses chunked encoding. This means that the message body contains one or more chunks of data. Each chunk consists of the chunk size in bytes (expressed in hexadecimal), followed by a newline, followed by the chunk contents. The message is terminated with a chunk of size zero. For example:

```HTTP
POST /search HTTP/1.1
Host: normal-website.com
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

b
q=smuggling
0
```

As the HTTP/1 specification provides two different methods for specifying the length of HTTP messages, it is possible for a single message to use both methods at once, such that they conflict with each other. The specification attempts to prevent this problem by stating that if both the`Content-Length`and`Transfer-Encoding`headers are present, then the`Content-Length`header should be ignored. This might be sufficient to avoid ambiguity when only a single server is in play, but not when two or more servers are chained together. In this situation, problems can arise for two reasons:

- Some servers do not support the`Transfer-Encoding`header in requests.
- Some servers that do support the`Transfer-Encoding`header can be induced not to process it if the header is obfuscated in some way.

If the front-end and back-end servers behave differently in relation to the (possibly obfuscated)`Transfer-Encoding`header, then they might disagree about the boundaries between successive requests, leading to request smuggling vulnerabilities.

#### Note

Websites that use HTTP/2 end-to-end are inherently immune to request smuggling attacks. As the HTTP/2 specification introduces a single, robust mechanism for specifying the length of a request, there is no way for an attacker to introduce the required ambiguity.

However, many websites have an HTTP/2-speaking front-end server, but deploy this in front of back-end infrastructure that only supports HTTP/1. This means that the front-end effectively has to translate the requests it receives into HTTP/1. This process is known as HTTP downgrading. For more information, see[Advanced request smuggling](https://portswigger.net/web-security/request-smuggling/advanced).

## How to perform an HTTP request smuggling attack

Classic request smuggling attacks involve placing both the`Content-Length`header and the`Transfer-Encoding`header into a single HTTP/1 request and manipulating these so that the front-end and back-end servers process the request differently. The exact way in which this is done depends on the behavior of the two servers:

- CL.TE: the front-end server uses the`Content-Length`header and the back-end server uses the`Transfer-Encoding`header.
- TE.CL: the front-end server uses the`Transfer-Encoding`header and the back-end server uses the`Content-Length`header.
- TE.TE: the front-end and back-end servers both support the`Transfer-Encoding`header, but one of the servers can be induced not to process it by obfuscating the header in some way.

#### Note

These techniques are only possible using HTTP/1 requests. Browsers and other clients, including Burp, use HTTP/2 by default to communicate with servers that explicitly advertise support for it during the TLS handshake.

As a result, when testing sites with HTTP/2 support, you need to manually switch protocols in Burp Repeater. You can do this from the**Request attributes**section of the**Inspector**panel.

### CL.TE vulnerabilities

Here, the front-end server uses the`Content-Length`header and the back-end server uses the`Transfer-Encoding`header. We can perform a simple HTTP request smuggling attack as follows:

```HTTP
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 13
Transfer-Encoding: chunked

0


SMUGGLED
```

The front-end server processes the`Content-Length`header and determines that the request body is 13 bytes long, up to the end of`SMUGGLED`. This request is forwarded on to the back-end server.

The back-end server processes the`Transfer-Encoding`header, and so treats the message body as using chunked encoding. It processes the first chunk, which is stated to be zero length, and so is treated as terminating the request. The following bytes,`SMUGGLED`, are left unprocessed, and the back-end server will treat these as being the start of the next request in the sequence.

### TE.CL vulnerabilities

Here, the front-end server uses the`Transfer-Encoding`header and the back-end server uses the`Content-Length`header. We can perform a simple HTTP request smuggling attack as follows:

```HTTP
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0
```

#### Note

To send this request using Burp Repeater, you will first need to go to the Repeater menu and ensure that the "Update Content-Length" option is unchecked.

You need to include the trailing sequence`\r\n\r\n`following the final`0`.

The front-end server processes the`Transfer-Encoding`header, and so treats the message body as using chunked encoding. It processes the first chunk, which is stated to be 8 bytes long, up to the start of the line following`SMUGGLED`. It processes the second chunk, which is stated to be zero length, and so is treated as terminating the request. This request is forwarded on to the back-end server.

The back-end server processes the`Content-Length`header and determines that the request body is 3 bytes long, up to the start of the line following`8`. The following bytes, starting with`SMUGGLED`, are left unprocessed, and the back-end server will treat these as being the start of the next request in the sequence.

### TE.TE behavior: obfuscating the TE header

Here, the front-end and back-end servers both support the`Transfer-Encoding`header, but one of the servers can be induced not to process it by obfuscating the header in some way.

There are potentially endless ways to obfuscate the`Transfer-Encoding`header. For example:

```HTTP
Transfer-Encoding: xchunked

Transfer-Encoding : chunked

Transfer-Encoding: chunked
Transfer-Encoding: x

Transfer-Encoding:[tab]chunked

[space]Transfer-Encoding: chunked

X: X[\n]Transfer-Encoding: chunked

Transfer-Encoding: chunked
```

Each of these techniques involves a subtle departure from the HTTP specification. Real-world code that implements a protocol specification rarely adheres to it with absolute precision, and it is common for different implementations to tolerate different variations from the specification. To uncover a TE.TE vulnerability, it is necessary to find some variation of the`Transfer-Encoding`header such that only one of the front-end or back-end servers processes it, while the other server ignores it.

Depending on whether it is the front-end or the back-end server that can be induced not to process the obfuscated`Transfer-Encoding`header, the remainder of the attack will take the same form as for the CL.TE or TE.CL vulnerabilities already described.

## How to identify HTTP request smuggling vulnerabilities

Check out the following section for some tips on how to identify HTTP request smuggling vulnerabilities for yourself. We've also provided some interactiveLABS, so you can see how this works in practice.

#### Read more

- [Finding HTTP request smuggling vulnerabilities](https://portswigger.net/web-security/request-smuggling/finding)

## How to exploit HTTP request smuggling vulnerabilities

Now that you're familiar with the basic concepts, let's take a look at how HTTP request smuggling can be used to craft a number of high-severity attacks. As usual, there are plenty of fully interactiveLABS, so you can try your hand at attacking realistic targets.

#### Read more

- [Exploiting HTTP request smuggling vulnerabilities](https://portswigger.net/web-security/request-smuggling/exploiting)

## Advanced HTTP request smuggling

If you've already completed the rest of our request smuggling labs, you're ready to learn some more advanced techniques. We've created a number of interactive LABS based on real-world vulnerabilities discovered by PortSwigger researchers. You'll even get a chance to try out Burp's one-of-a-kind features for HTTP/2-based testing.

#### Read more

- [Advanced HTTP request smuggling vulnerabilities](https://portswigger.net/web-security/request-smuggling/advanced)

## Browser-powered request smuggling

The request smuggling techniques you've learned so far rely on sending intentionally malformed requests using dedicated hacking tools like Burp Repeater. In fact, it's possible to perform the same attacks using fully browser-compatible requests that desync the two servers using a perfectly normal`Content-Length`header.

This even enables you to launch client-side variations of these attacks, which induce a victim's browser to poison its own connection to the vulnerable website. Not only does this expose single-server sites to request smuggling-style attacks, it even enables you to attack sites that you don't have access to directly. Check out the learning materials andLABSto learn how.

#### Read more

- [Browser-powered request smuggling](https://portswigger.net/web-security/request-smuggling/browser)

## How to prevent HTTP request smuggling vulnerabilities

HTTP request smuggling vulnerabilities arise in situations where the front-end server and back-end server use different mechanisms for determining the boundaries between requests. This may be due to discrepancies between whether HTTP/1 servers use the`Content-Length`header or chunked transfer encoding to determine where each request ends. In HTTP/2 environments, the common practice of[downgrading HTTP/2 requests](https://portswigger.net/web-security/request-smuggling/advanced/http2-downgrading)for the back-end is also fraught with issues and enables or simplifies a number of additional attacks.

To prevent HTTP request smuggling vulnerabilities, we recommend the following high-level measures:

- Use HTTP/2 end to end and disable HTTP downgrading if possible. HTTP/2 uses a robust mechanism for determining the length of requests and, when used end to end, is inherently protected against request smuggling. If you can't avoid HTTP downgrading, make sure you validate the rewritten request against the HTTP/1.1 specification. For example, reject requests that contain newlines in the headers, colons in header names, and spaces in the request method.
- Make the front-end server normalize ambiguous requests and make the back-end server reject any that are still ambiguous, closing the TCP connection in the process.
- Never assume that requests won't have a body. This is the fundamental cause of both CL.0 and client-side desync vulnerabilities.
- Default to discarding the connection if server-level exceptions are triggered when handling requests.
- If you route traffic through a forward proxy, ensure that upstream HTTP/2 is enabled if possible.

As we've demonstrated in the learning materials, disabling reuse of back-end connections will help to mitigate certain kinds of attack, but this still doesn't protect you from[request tunnelling](https://portswigger.net/web-security/request-smuggling/advanced/request-tunnelling)attacks.

#### Read more

- [Find HTTP request smuggling vulnerabilities using Burp Suite's web vulnerability scanner](https://portswigger.net/burp/vulnerability-scanner)
