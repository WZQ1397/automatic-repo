#!/bin/bash
PATH=/usr/local/sbin/
PDB_LOC=/etc/pureftpd.pdb
cmd=$1
start(){
  $PATH/pure-ftpd -j -lpuredb:$PDB_LOC &
  }
stop(){
  PID=`ps aux | grep pure | grep -i SERVER | awk -F " " '{print $2}'`
  kill $PID
}
case "$cmd" in
start)
    start
    ;;
stop)
    stop
    ;;
reload)
    pure-pw mkdb
    ;;
restart)
    start
    stop
    ;;
esac
if [ $? -eq 0 ];
then
  echo $cmd " is ok!"
else
  echo $cmd " is ERROR!"
fi

if [ $cmd -eq "start" ];
then
  read -p "DO you want to exit terminal [y/n]?" choice
  if [ `echo $choice | grep -qi "y"` ];
  then
    echo "ok"
    sleep 2
    exit
  fi
fi