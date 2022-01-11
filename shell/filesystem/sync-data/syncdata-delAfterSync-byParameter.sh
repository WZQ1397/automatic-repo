src=$1
dst=$2
targetsvc="6.6.6.6:58122"
if [[ $# -ge 2 ]] && [[ $# -le 3 ]];
then
  if [[ $# -eq 3 ]];
  then
    targetsvc=$3
  fi
  echo "starting ..."
else
  echo "Parameter not enough, EG: $0 /data/imgs /data/ocr/999-jklaaa $targetsvc"
  exit -1
fi
port=`echo $targetsvc | cut -d ':' -f 2`
addr=`echo $targetsvc | cut -d ':' -f 1`
echo "send to server $addr, port $port"
sshpass -p rlogs rsync --remove-source-files -avzP -e "ssh -p $port" $src rlogs@$addr:/$dst
du -sh $src