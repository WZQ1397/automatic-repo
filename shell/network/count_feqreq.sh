#!/bin/bash 
# 
# Filename:  count_req.sh 
# Description: 统计Nginx日志里IP访问频率 
 
NGINXLOG="./access.log"
start_time=$(head -n1 "$NGINXLOG" | grep -o " \[.*\] ") 
stop_time=$(tail -n1 "$NGINXLOG" | grep -o " \[.*\] ") 
echo -e "start:\t\e[92m$start_time\033[0m"
echo -e "stop:\t\e[92m$stop_time\033[0m"
echo '所有的请求TOP50-->>'
# 所有的请求 
cat "$NGINXLOG" | awk '{++S[$1]} END {for(a in S) print S[a],"\t", a}' | sort -rn -k1 | head -n 50 
echo '--------------------------------------------------'
echo '成功的请求TOP50-->>'
# 成功的请求 
grep ' 200 ' "$NGINXLOG" | awk '{++S[$1]} END {for(a in S) print S[a],"\t", a}' | sort -rn -k1 | head -n 50 

#for ip in `grep ' 200 ' "$NGINXLOG" | awk '{++S[$1]} END {for(a in S) print S[a],"\t", a}' | sort -rn -k1 | head -n 10`
#do
#iptables -I INPUT -s ${ip} -j DROP
#done