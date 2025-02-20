# Support repo: local DNS tests, DNS comparisson and more

## Looking for a suspect failing DNS server

### Check for lost packages
`
ping -c 50 8.8.8.8
`
### Manual test first with publick well known DNS servers:
`
dig @8.8.8.8 www.google.com | grep time
dig @1.1.1.1 www.google.com | grep time
dig @1.0.0.1 www.google.com | grep time
dig @9.9.9.9 www.google.com | grep time
`
#### Test via TCP
`
dig +tcp @8.8.8.8 www.google.com
`
#### Test with parallel queries
`
for i in {1..10}; do dig @207.138.36.249 www.google.com & done
wait
`
#### Test different Query Types
`
dig @207.138.36.249 www.google.com A
dig @207.138.36.249 www.google.com AAAA
dig @207.138.36.249 www.google.com ANY
`
#### Avoid rate limiting while manually testing
`while true; do dig @207.138.36.249 www.google.com | grep time; sleep 5; done`

### Check Traceroute
`
traceroute 8.8.8.8
`
### Check your firewall
`
sudo iptables -L -n | grep 53
sudo ufw status
`
### Check your resolver for resolution problems.
`
resolvectl status
`

Check if you are using you trash modem-router for DNS resolution, check for something like:

`
Global
         Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
  resolv.conf mode: stub

Link 2 (eno1)
    Current Scopes: DNS
         Protocols: -DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 192.168.6.1
       DNS Servers: 192.168.6.1
        DNS Domain: hikvisionwifi.local
`

#### Check your internet connection speed
curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -


#### Check your PC for network congestion

`netstat -antup | grep ESTABLISHED`

#### Check your WiFi strenght

check for lower values -70 dBm:

`iwconfig wlo1`

# Finally, override your DNS on your PC
`sudo nano /etc/systemd/resolved.conf`

a common approach is to set-up the Cloudflare DNS, or search-test for the best with the script on this repo
`
[Resolve]
DNS=1.1.1.1 9.9.9.9
FallbackDNS=8.8.8.8
`

## Compare DNSs around you

#### Run test_dns.sh

Go to the web and take the DNS list around you, then:

1- Take the full list of IPs of DNS around you:
https://publicdnsserver.com/venezuela/#listnegoro

2- download the IP list from the link on the page, in that case:
https://publicdnsserver.com/download/venezuela.txt

3- Enrich the list with ASN, carrier and Reliablity info from:
https://public-dns.info/nameserver/ve.html

4 - Edit the test_dns script with the data, then run it to generate the json:
`
chmod +x test_dns.sh
./test_dns.sh dns_list.txt
`

5- Best DNS around you is shown. You can also check the results.csv with detailed results.

6- You can grab the screen with the list as shown IP,MS and graph it with the support script on ./graph, just modified the script a litle.

Check for ./graph/README.md for more instructions.

![plot](./graph/visualization.png)
