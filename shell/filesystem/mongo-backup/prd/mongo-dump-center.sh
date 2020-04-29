#!/bin/sh
export PATH=/data/app/mongodb/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin
dir=/data/bak/monbak
date=`date +%Y%m%d`
time=`date +%Y%m%d_%H%M%S`
dirlog=/data/bak/monlog
firstlog=${dirlog}/first_record.log
lastlog=${dirlog}/last_record.log
baklog=${dirlog}/monbak.log
resultlog=${dirlog}/result/monresult_${time}.log
rlog=`ls ${dirlog}/mon*bak_${date}_*.log`
dbname=hw_report
host=mongodb
 
mongo_args=(
        "127.0.0.1:6668/local"
        "--authenticationDatabase admin"
        " -u hw"
        "-p 123456"
  )
 
bak_args=(
        "-h 127.0.0.1"
        "--port 6668"
        "--authenticationDatabase admin"
        "-u hw"
        "-p 123456"
        "--gzip"
  )
 
#第一个
first=$(mongo ${mongo_args[@]} --eval "db.oplog.\$main.find({'ns':{\$regex:\"${dbname}\"}}).limit(1);"|grep Timestamp|awk -F '[{":(,)]' '{print $6","$7}')
 
#最后一个
last=$(mongo ${mongo_args[@]} --eval "db.oplog.\$main.find({'ns':{\$regex:\"${dbname}\"}}).sort({ts:-1}).limit(1)"|grep Timestamp|awk -F '[{":(,)]' '{print $6","$7}')
 
full(){
  baktype=full
  starttime=`date +%s`
  mongodump ${bak_args[@]} --oplog -o ${dir}/${host}_${baktype}_${time}
  stoptime=`date +%s`
  costtime=`expr ${stoptime} - ${starttime}`
}
 
inc(){
  baktype=inc
  first=`tail -n1 ${lastlog}`
  starttime=`date +%s`
  mongodump ${bak_args[@]}  -d local -c "oplog.\$main" -q "{ts:{\$gt:Timestamp(${first}),\$lte:Timestamp(${last})},ns:/^${dbname}\\\./}" -o ${dir}/${host}_${baktype}_${time}
  stoptime=`date +%s`
  costtime=`expr ${stoptime} - ${starttime}`
}
 
record(){
  datefirst=$(date "+%Y-%m-%d %H:%M:%S" -d @`echo ${first}|awk -F '[,]' '{print $1}'`)
  datelast=$(date "+%Y-%m-%d %H:%M:%S" -d @`echo ${last}|awk -F '[,]' '{print $1}'`)
  if [ ${baktype} == 'inc' ];then
    count=`grep 'done dumping local.oplog.' ${rlog} |awk '{for (i=2;i<=NF;i++)printf("%s ", $i);print ""}'`
    printf "%-24s [%s] [%s %s]\n"  "|--${baktype}_${time}:" "first:(${first}) <  oplog <= last:(${last})" "${datefirst} ~ ${datelast}" "${count}"  >> ${baklog}
  else
    echo "" >> ${baklog}
    count=`grep 'done dumping hw_report.kj_report' ${rlog} |awk '{for (i=2;i<=NF;i++)printf("%s ", $i);print ""}'`
    printf "%-24s [%s] [%s %s] \n"  "${baktype}_${time}:" "first:(${first}) <= oplog <= last:(${last})" "${datefirst} ~ ${datelast}" "${count}"  >> ${baklog}
  fi
  echo ${first} >> ${firstlog}
  echo ${last} >>  ${lastlog}
}
 
result(){
   echo "[backup]" >> ${resultlog}
   echo "备份目标: ${host} mongodb" >> ${resultlog}
   echo "备份类型: ${baktype}" >> ${resultlog}
   echo "备份开始时间: ${time}" >> ${resultlog}
   echo "备份持续时间: ${costtime}s" >> ${resultlog}
   echo "备份目录名称: ${host}_${baktype}_${time}" >> ${resultlog}
   echo "备份目录大小: `du -s ${dir}/${host}_${baktype}_${time}|awk '{print $1}'`k" >> ${resultlog}
   br=`echo ${count}|grep "done dumping"|wc -l`
   [ ${br} -eq 1 ]&&r=SUCCESS||r=FAILED
   echo "备份结果: ${r}" >> ${resultlog}
}
 
 
after(){
  #定期删除备件文件    
  #find ${dir} -type d -mtime +12 | xargs rm -rf
}
 
 
case $1 in
full)
  full
  record
  result
;;
inc)
  inc
  record
  result
;;
*)
  echo "$0 {full|inc}"
;;
esac