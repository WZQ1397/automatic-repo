src=$1
dst=$2
targetsvc="6.6.6.6:18008"
if [[ $# -ge 2 ]] && [[ $# -le 3 ]];
then
  if [[ $# -eq 3 ]];
  then
    targetsvc=$3
  fi
  echo "starting ..."
else
  echo "Parameter not enough, EG: $0 /data/imgs /data/ocr/999-jklaaa 6.6.6.6:18008"
  exit -1
fi
port=`echo $targetsvc | cut -d ':' -f 2`
addr=`echo $targetsvc | cut -d ':' -f 1`
echo "send to server $addr, port $port"
rsync -avzP -e "ssh -p $port" $src dev@$addr:/$dst
