echo '1' >/proc/sys/net/ipv4/ip_forward
sysctl -p
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -P INPUT DROP
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -A INPUT  -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -t nat -A POSTROUTING -s 1.1.1.1 -j SNAT --to-source 2.2.2.2
iptables -t nat -A PREROUTING -d 2.2.2.2 -j DNAT --to-destination 1.1.1.1
iptables -t nat -A PREROUTING -p tcp -d 1.1.1.1 --dport 8080 -j DNAT --to 1.1.1.1:80
iptables-save
