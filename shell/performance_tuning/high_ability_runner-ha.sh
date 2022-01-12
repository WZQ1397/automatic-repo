SERV_A="157.0.0.1"
SERV_B="192.168.1.124"
PORT=10002
SERVLST=($SERV_A $SERV_B)
ind=0
function ha_chk(){
  NOW_SERV=$1
  NEXT_SERV=$2
  count=5
  while [[ $count -gt 0 ]];
  do
    curl -s -I $NOW_SERV:$PORT
    if [[ $? -eq 0 ]];
    then
      exit 0
    fi
    let "count--"
    sleep 5
  done
  sed "s/\(.*\)=\(.*\)/\1=$NEXT_SERV/g" /etc/profile
}


while [[ $ind -lt ${#SERVLST[@]} ]];
do
   NOW_SERV=${SERVLST[$ind]} 
   if [[ $ind+1 -ge ${#SERVLST[@]} ]];
   then
     NEXT_SERV=${SERVLST[0]}
   else
     NEXT_SERV=${SERVLST[$ind+1]}
   fi
   ha_chk $NOW_SERV $NEXT_SERV
   let "ind++"
done
