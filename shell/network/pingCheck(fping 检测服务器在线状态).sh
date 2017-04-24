# yum -y install fping 
#!/bin/bash
# Filename: pingCheck.sh

# IP 前缀
IP_PRE="1.1.1"

function pingStatus() {
    fping -c5 -a $1
    return $?
}

echo "[*] 服务器公网IP状态[只输出异常]"
printf "%-5s %-20s %6s \n" [+] 'IP Address' Status
for i in {33..46}
do
    IP=${IP_PRE}.${i}
    pingStatus ${IP} >/dev/null 2>&1 || \
    printf "%-5s %-20s %6s \n" [-] ${IP}  Dead &
done
wait