# Micro-CMS v2

As an Anonymous user, we can access 2 **public post** and then try to access another post by change the ID, we got the post 3 with a 403 message.

Try to change the method on /post/3, but it cannot work, then change the method on /post/edit/3 to PUT and we got the FLAG



We have a login page, then try to login as admin but we cannot access.
Try to SQL injection, we got the username have SQL injection vuln.

But we cannot log in, it's notice that Invalid password. We can guess that we have 2 part to check the user.
First, find the username, and then compare the password.

It can be done with a simple logic like: make a query to get the password that match with the user. Then compare the password.

Try to confuse it by add a another value in the query result like

username=admin'+union+select+'hacker&password=hacker

And we can login successfully, go to private page and we got FLAG

After login successfully we got something like this:

```html
<script>setTimeout(function() { window.location = 'home'; }, 3000);</script>
<!-- You got logged in, congrats!  Do you have the real username and password?  If not, might want to do that! -->
```

Then we try to use sqlmap to dump the database and retrieve real username/password

# Photo Gallery

GET /fetch?id=4+UNION+SELECT+'uwsgi.ini'-- HTTP/2

SQLmap

