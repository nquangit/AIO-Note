## What is the SSH?

SSH stands for **Secure Shell**. The term "SSH" can refer to both the SSH protocol and the software tools that enable system administrators and users to establish secure connections to remote computers using this protocol.

The SSH protocol is an encrypted protocol designed to provide a secure connection over an insecure network, such as the internet. In Linux, SSH is based on a portable version of the OpenSSH project. It follows a classic **client-server model**, with an SSH server accepting connections from SSH clients. The client connects to the server and displays the session to the remote user, while the server accepts the connection and executes the session.

## The need of securing SSH

By default, an SSH server listens for incoming connections on Transmission Control Protocol (TCP) port 22. Since this is a well-known standardized port, it is often targeted by threat actors and malicious bots.

Threat actors deploy bots that scan a range of IP addresses looking for open ports. These ports are then tested for vulnerabilities that can be exploited. Assuming "I'm safe because there are bigger and better targets than me" is a misconception. The bots are not choosing targets based on merit; they are systematically searching for any systems they can infiltrate.

If you haven't secured your system, you are essentially nominating yourself as a potential victim.

## Some method can be used for securing SSH

### Avoid default port (22)

Port 22 is the default port for SSH connections. Using a different port can add a minor layer of security through obscurity. While security through obscurity is not considered a legitimate security measure and has been criticized in other articles, it can still be somewhat beneficial. Some advanced attack bots scan all open ports to identify the services running on them, rather than just relying on a standard port list. However, using a non-standard port can reduce the amount of unwanted traffic and noise typically directed at port 22.

 To configure a non-standard port, edit your SSH configuration file:
 
```bash
sudo vim /etc/ssh/sshd_config 
# Or
sudo nano /etc/ssh/sshd_config
# Or any editor you want
```
 
 ![image](https://hackmd.io/_uploads/SyFBak3_R.png)
 https://hackmd.io/_uploads/SyFBak3_R.png

Then save your configuration file and restart the SSH daemon:

```bash
sudo systemctl restart sshd
# And/Or
sudo systemctl restart ssh
```

Connect to the SSH server using the new port

```bash
ssh -p <port> username@host
```

### Use SSH Key-Based Authentication

SSH key-based authentication provides a more secure alternative to password-based authentication. Instead of using a password, users generate a public-private key pair. The public key is placed on the server, while the private key remains on the client. When a user attempts to connect, the server uses the public key to verify the private key, allowing access only if they match.

To set up SSH key-based authentication:

1. Generate the SSH Key Pair:

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

This command generates a 4096-bit RSA key pair. You can also use other algorithms like ECDSA or Ed25519 for even stronger security.

1. Copy the Public Key to the Server:

```bash
ssh-copy-id username@remote_host
```

This command copies your public key to the server, placing it in the ~/.ssh/authorized_keys file of the specified user.

### Disable Password Authentication:

Edit the SSH configuration file on the server:

```bash
sudo vim /etc/ssh/sshd_config
```

Set the following directive:

```bash
PasswordAuthentication no
```

Restart the SSH daemon to apply the changes:

```bash
sudo systemctl restart sshd
# And / Or
sudo systemctl restart ssh
```

### Disable Root Login

Disabling root login adds an extra layer of security by requiring users to log in with a regular user account before elevating privileges using sudo. This reduces the risk of brute-force attacks targeting the root account.

To disable root login, edit the SSH configuration file:

```bash
sudo vim /etc/ssh/sshd_config
```

Set the following directive:

```bash
PermitRootLogin no
```

Restart the SSH daemon:

```bash
sudo systemctl restart sshd
```

### Limit Access by IP Address

Restricting access to the SSH server to specific IP addresses can prevent unauthorized access. This can be achieved using firewall rules or TCP Wrappers.

1. Using TCP Wrappers:

Edit the /etc/hosts.allow file to allow only specific IP addresses:

```bash
sshd: 192.168.1.0/24
```

Deny all other IP addresses in the /etc/hosts.deny file:

```bash
sshd: ALL
```

1. Using a Firewall:

Configure your firewall (iptables or ufw) to allow SSH connections only from specific IP addresses.

- Using UFW:

    ```bash
    sudo ufw allow from 192.168.1.0/24 to any port 22
    sudo ufw enable
    ```
- Using iptables:

    ```bash
    sudo iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 22 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 22 -j DROP
    ```

### Enable Two-Factor Authentication (2FA)

Adding two-factor authentication (2FA) significantly enhances security by requiring a second form of verification in addition to the SSH key or password.

1. Install Google Authenticator:

```bash
sudo apt-get install libpam-google-authenticator
```

1. Configure SSH to Use 2FA:

Edit the PAM configuration file for SSH:

```bash
sudo vim /etc/pam.d/sshd
```

Add the following line:

```bash
auth required pam_google_authenticator.so nullok
auth required pam_permit.so
# And comment this line
#@include common-auth
```

1. Edit the SSH Configuration File:

```bash
sudo vim /etc/ssh/sshd_config
```

Ensure the following directives are set:

```bash
ChallengeResponseAuthentication yes

AuthenticationMethods publickey,password publickey,keyboard-interactive
```

Restart the SSH daemon:

```bash
sudo systemctl restart sshd
```

1. Set Up Google Authenticator on Your Account:

Run the Google Authenticator setup:

```bash
google-authenticator
```

Follow the prompts to configure and secure your account with 2FA.

### Keep SSH Updated

Regularly updating your SSH software ensures you have the latest security patches and features. Use your package manager to update OpenSSH:

On Debian-based systems (e.g., Ubuntu):

```bash
sudo apt-get update
sudo apt-get upgrade openssh-server
```

On Red Hat-based systems (e.g., CentOS):

```bash
sudo yum update openssh-server
```

By applying these methods, you can significantly enhance the security of your SSH connections, protecting your systems from unauthorized access and potential attacks.

