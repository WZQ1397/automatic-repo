#!/bin/bash
# Author: Zach.Wang
# DESC: Auto login to jumperserver
select env in f5 dev prd
do
  case $env in
  "f5"|"prd")
        key="AAAA"
  	host="usws00mgt001.usws00.com"
	break
	;;
  "dev")
        key="BBBB"
  	host="uses01mgt001.uses01.com"
	break
	;;
  *)
  	echo "$0 [env]"
	exit
  esac
done

CMD="sshpass -p ${key} ssh "
echo "You select $env:"

$CMD zhwang@$host
