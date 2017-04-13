#!/bin/bash
#        Author: Zach.Wang
#        Create: 2017-04-13 20:40:37
[ -f /etc/init.d/functions ] && source /etc/init.d/functions
#check_url
wait(){
echo -n "wait 3s"
for((i=0;i<3;i++))
do
  echo -n "."
  sleep 1
done
echo 
}
check_url(){
  wget -T 5 -t 2 --spider $1 &>/dev/null
  RETVAL=$?
  if [ $RETVAL -eq 0 ];then
      action "check $1"  /bin/true
  else
      action "check $1"  /bin/false   
  fi
  return $RETVAL
}
main(){
  wait
  while read line
  do
    check_url $line
  done < list.txt
}
main