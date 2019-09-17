#!/bin/bash
home_prefix="/home/mobile"
midpath="/home/upload/hb/send"
starttime=`date +%Y%m%d`
TmpDateFile="date.tmp.$starttime"
TmpMonthFile="month.tmp.$starttime"
resultFile="createlog.zach"


function usage(){
cat <<'EOF'

###########################################################
#  Author     : zach.wang                                 #
###########################################################
Usage: $0 [OPTION]... LAST
       -s start time : must be the first choice
       must choose -d or -m
       -d create by days
       -m create by months
EOF
}


function generateDate(){
first=$starttime
second=$finaltime
while [ "$first" != "$second" ]
do
echo $first >> $TmpDateFile
let first=`date -d "-1 days ago ${first}" +%Y%m%d`
done
}

function generateMonth(){
first=""
second=`echo ${finaltime:0:4}/${finaltime:4:2}`
i=1
while [ "$first" != "$second" ]
do
echo $first >> $TmpMonthFile
first=`date -d " -$i month ago" +%Y/%m`
i=$(($i+1))
#echo $i
done
}

function CreateByDate(){
generateDate
cat $TmpDateFile | while read line
do
  path="$home_prefix$midpath/$line"
  echo $path >> $resultFile
  mkdir -pv $path
done
}

function CreateByMonth(){
generateMonth
cat $TmpMonthFile | while read line
do
  lst=("block" "credit")
  for x in ${lst[@]}
  do 
    path="$home_prefix$midpath/$x/$line"
    echo $path >> $resultFile
    mkdir -pv $path
  done
done
}

function cleanTmp(){
   rm -rf $TmpDateFile $TmpMonthFile
}

function mkDir(){
   mkdir -pv $1
}

cleanTmp
> $resultFile
leftstr=$(printf "%-10s" "=+")
rightstr=$(printf "%-10s" "+=")
echo "${leftstr// /=+} $starttime ${rightstr// /+=}" >> $resultFile

while getopts :dms:h opt
do
 case $opt in
 d) CreateByDate;;
 m) CreateByMonth;;
 s) finaltime=$OPTARG;;
 h) usage ;;
 *) usage ;;
 esac
done
if [[ -z $finaltime ]];
then
finaltime="date -d "next-year" +%Y%m%d"
fi
