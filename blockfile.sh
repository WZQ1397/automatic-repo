#!/bin/bash
#HOW TO 
#./createfile.sh aaa 10 50 bin /aaa
NAME=$1
MYPATH=$5
START=$2
END=$3
TAIL=$4


[ -z $MYPATH ] && MYPATH=/zach_dir/

[ -d $MYPATH ] || mkdir $MYPATH


for (( i = $START ; i <= $END;i++ ))
do
     PERFIX=`< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c12`
     echo $MYPATH/${PERFIX}_$NAME-$i.$TAIL
     touch $MYPATH/${PERFIX}_$NAME-$i.$TAIL
done

