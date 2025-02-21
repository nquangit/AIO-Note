# Information

> Simple Storage Service

S3 bucket is like a big, virtual box where you can store all sorts of things like pictures, videos, and other files.

Imagine you have a big toy box at home where you keep all your toys organized. Similarly, an S3 bucket is a virtual box where you can keep all your digital things organized. You can even keep your toys safe in the toy box, and in the same way, you can keep your important digital files safe in an S3 bucket.

You can access your S3 bucket from anywhere in the world as long as you have an internet connection. This means that you can store and access your things from any computer or device that has internet access.

S3 buckets are used by many companies and individuals to store and share files and information over the internet. And just like a toy box, you can choose to share your things with others or keep them private for your own use.

## Style

- Virtual-Hosted Style

`https://name_of_bucket.s3.reigon.amazonaws.com/key_name`
Ex: `https://secret-bucket.s3.ap-south-1.amazonaws.com/file.txt`

- Path Style

`https://s3.region.amazonasw.com/name_of_bucket/key_name`
Ex: `https://s3.ap-south-1.amazonaws.com/secret-bucket/index.html`


# Vulnerability

## Unrestricted File Upload

Change the `GET` HTTP method to PUT with a file body content


## Authenticated User can read files

Anonymous User cannot read the files but an authenticated can read from the aws cli

## Bucket Takeover

**Scenario**: Developer forget to remove CNAME record from Route53 and attacker has claimed s3 bucket.

Use `dig` to find out the s3 bucket name and then check if that exist.

Then try to create a new one with the same name (if the s3 bucket name was found above doesn't exist) and configure the policies to accept the target URL/domain.

