from IPy import IP

ipaddr = "192.168.1.0/28"
ips = IP(ipaddr)
print("总IP个数",ips.len(),"\n",ips.netmask(),ips.broadcast())
for x in ips:
    print(x,"\t",x.reverseName(),x.iptype())
    # TODO 相反IP()数进制
    print(x.strHex(),x.strBin())

#check IP
ipad = '192.168.10.0'
print(IP(ipad).make_net(18) == IP(ipad+"/255.255.192.0",make_net=True))
print(IP(ipaddr).strNormal(0))
print(IP(ipaddr).strNormal(2))
print(IP(ipaddr).strNormal(3))

print(bool(IP('192.168.0.0/23').overlaps('192.168.1.0/24')))
print('192.168.1.100' in IP('192.168.1.0/24'))
print(IP('10.0.0.0/24') < IP('12.0.0.0/24'))