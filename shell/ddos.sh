#!/bin/bash
  
log=/tmp/tmp.log
  
[ -f $log ] || touch $log
  
function add_iptables(){
    whileread line
        do
          ip=`echo $line|awk '{print $2}'`
          count=`echo $line|awk '{print $1}'`
            if [ $count -gt 100 ] && [`iptables -L -n|grep "$ip"|wc -l` -lt 1 ]
             then
                iptables -I INPUT -s $ip -jDROP
                echo "$line isdropped" >>/tmp/droplist.log
            fi
        done<$log
}
  
  
function main(){
    whiletrue
           do
             #awk '{print $1}' access.log|grep-v "^$"|sort|uniq -c >$log
             netstat -an|grep EST|awk -F '[:]+' '{print $6}'|sort|uniq -c >$log
             add_iptables
             sleep 180
    done
}
  
main