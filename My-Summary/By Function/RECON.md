Use Tools e.g. [Asnlookup](https://github.com/yassineaboukir/Asnlookup) OR  
Service [host.io](https://host.io/company.com) To Get List Of CIDR

```bash
python3 asnlookup.py -o Organization
# #-o Organization " Name Of Organization To Enumerate
```

Use Tools e.g. [dnsx](https://github.com/projectdiscovery/dnsx) To Get  
Subdomains From Reverse DNS Lookups

```bash
cat cidrs.txt | ./mapcidr -silent -o out.txt
cat out.txt | sort -u | tee -a ips.txt
cat ips.txt | dnsx -r resolvers.txt -ptr -silent -resp-only | tee -a subdomains.txt

# " -r resovers.txt " Input File Of IPs DNS Resolver
# " -ptr " Query PTR Record
# " -silent " Silent Mode To Show Only Results
# " -resp-only " Display Only Response Data
```

Use Tools e.g. [hakrevdns](https://github.com/hakluke/hakrevdns) To Get  
Subdomains From Reverse DNS Lookups

```bash
root@mine:~#cat reverseDNS.sh
#!/usr/bin/env bash
for i in `cat cidrs.txt`
do
 	prips $i | ./hakrevdns -d -r 1.1.1.1 | tee -a subdomains.txt
done
root@mine:~#./reverseDNS.sh

# " prips I.P.v.4/cidr " Print All Of The IP Addresses
# " -r 1.1.1.1 " IP Of The DNS Resolver
```

Use Tools e.g. [masscan](https://github.com/robertdavidgraham/masscan) To Scan  
What IPs Have HTTPS Certificate

```bash
masscan -iL ips.txt --source-port 53 --http-user-agent "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77" -p 443 -oL httpservice443alive.txt

# " -iL input.txt " Reading Input File
# " --source-port 53 " Use A Custom Source Port
# " --http-user-agent "Mozilla" " Custom User Agent
# " -oL httpservice443alive.txt " Output File
```

Use Tools e.g. [SANextract](https://github.com/hvs-consulting/SANextract) To Get  
 Subject Alternative Names

```bash
cat  httpservice443alive.txt | ./SANextract -timeout 30s | tee -a subdomains.txt
```

Try To Discover What IPs Are Up By Using Tools e.g. [nmap](https://nmap.org/)  
To Minimize Time Of Full PORTs Scanning

```bash
nmap -sP -PE -PP -PS21,22,23,25,80,113,31339 -PA80,113,443,10042 --source-port 53 -T4 -iL ips.txt
```

Full PORTs Scanning With SYN Scan

```bash
nmap -sSV --version-intensity 9 --min-parallelism 64 --min-hostgroup 16 --max-hostgroup 64 --max-retries 3 --min-rate 175 --max-rate 300 -Pn -n --source-port 53 --mtu 24 --data-length 25 --script-args http.useragent="Mozilla/5.0" --max-scan-delay 10 -p- -iL ips.txt -oA output

nmap -sSV --version-intensity 9 -PN -n --max-rtt-timeout 1000ms --min-parallelism 1000 --max-retries 3 --source-port 53 --mtu 24 --data-length 25 --script-args http.useragent="Mozilla/5.0"  
-p- -iL ips.txt -oA output
```

Use Tools e.g. [subgen](https://github.com/pry0cc/subgen) To Generate  
Wordlist Based On Names Of Subdomains

