find_ip = $1
count = $2

if  [ ! -n "$1" ] ;then
    echo "WRONG SYNTAX!"
    echo "Uasge: find_dup_ip.sh $find_ip [$count]"
    exit -1
fi

function IPRelatedSkills()
{
  if [ ! -n "$count" ];
  then 
    count = 2
  fi
  
  sudo arping -D -I eth0 -c $count $find_ip
  if [ $? == 0 ];
  then
    echo "It has duplicate IP"
  fi
}

IPRelatedSkills