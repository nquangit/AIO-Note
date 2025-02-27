> https://medium.com/@lightbulbr/install-burp-ca-as-a-system-level-trusted-ca-android-11-rooted-physical-device-5542fe96345f

Hello, in order to test the traffic for a mobile application I had to install Burp Certificate as CA. In order to do this in Android 11 I had to follow a different approach than the one I used to since the previous method does not work anymore.

All the CA certificates of Android are stored to the location /system/etc/security/cacerts. So, it is required to add the Burp Certificate in this directory.

Steps to install Burp CA:

The first step is to export the Burp Certificate and then convert it into the right format. As shown below, go to the Proxy->Options->Import/Export CA certificate and export the CA Certificate in DER format. I saved it as burp-latest.

Android wants the certificate to be in PEM format, and to have the filename equal to the subject_hash_old value appended with .0. Since the certificate is in DER format we need to convert it into PEM. This will be achieved using openssl.

Note: if you are using OpenSSL <1.0, it’s actually just the subject_hash, not the “old” one.

Output the result of openssl to the subject_hash_old and rename the file:

```bash
openssl x509 -inform DER -in burp-latest -out burp-latest.pem
openssl x509 -inform PEM -subject_hash_old -in burp-latest.pem | head -n -1
```

Copy the certificate to the device.

```bash
adb push <cert>.0 /sdcard/
```

The next step is to move the certificate to the location /system/etc/security/cacerts/. However, the /system location is read-only. We need to remount it as writable. This can be done with the command below:

```bash
a41:/ # mount -o rw,remount /system
```

While attempting this with my mobile device I encountered the error “mount: ‘/system’ not in /proc/mounts”.

All the mounted filesystems on the device can be found in /proc/mounts file. A simple cat can help us find the correct name of the location to mount.

```bash
a41:/ # cat /proc/mounts | grep -i ' / '
```

You will need to use the following command to remount the filesystem.

```bash
a41:/ # mount -o rw,remount /dev/block/dm-4 /
```

After successful remount of the system I used the below instructions as per this article to add Burp’s Certificate to the required location:

```bash
a41:/ # mkdir -m 700 /storage/emulated/0/<folder>
a41:/ # cp /system/etc/security/cacerts/* /storage/emulated/0/<folder>
a41:/ # mount -t tmpfs tmpfs /system/etc/security/cacerts
a41:/ # mv /storage/emulated/0/<folder>/* /system/etc/security/cacerts/
a41:/ # mv /sdcard/<old_hash>.0 /system/etc/security/cacerts/<old_hash>.0
a41:/ # chown root:root /system/etc/security/cacerts/*
a41:/ # chmod 644 /system/etc/security/cacerts/*
a41:/ # chcon u:object_r:system_file:s0 /system/etc/security/cacerts/*
```
    
Don’t reboot.

Browsing to Settings -> Biometrics and Security -> Other security settings ->View security Certificates should show the new “Portswigger CA” as a system trusted CA.

Now it’s possible to set up the proxy and start intecepting any and all app traffic with Burp :)
References:

https://blog.ropnop.com/configuring-burp-suite-with-android-nougat/
https://www.hacknia.com/how-to-install-ca-cert-in-android-11/

    