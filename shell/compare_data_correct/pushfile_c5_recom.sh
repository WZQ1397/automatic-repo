#!/bin/bash

Public_path='/home/data2/cctvuser/app/c5data'
Output_path='/home/data2/cctvuser/app/c5data/backupdata'
Remote_path='/home/ftpdir/ziplog/app/c5data'
Remote_host='10.110.142.4'
hdfs_path='/user/cctvuser/ziplog/app/c5data'

function targz {
        echo ""
        echo "`date +%Y/%m/%d_%H:%M:%S` begin zip "$Public_path/$year/$month/$day" to "$Output_path/$year/$month/$day/${save_file}.zip
        mkdir -pv $Output_path/$year/$month/$day/ && \
        cd $Public_path/$year/$month/$day && \
        zip -r -9 -q $Output_path/$year/$month/$day/${save_file}.zip * >> /dev/null
        CMD_status=$?
        if [ $CMD_status -eq 0 ];then
                echo "`date +%Y/%m/%d_%H:%M:%S`end zip! begin rsync "$Output_path/$year/$month/$day/" to "cctvuser@${Remote_host}:$Remote_path/$year/$month/$day/
                /usr/bin/sshpass -p "1234" ssh -o "StrictHostKeyChecking=no" cctvuser@${Remote_host} mkdir -p $Remote_path/$year/$month/$day/ && \
                /usr/bin/sshpass -p "1234" rsync -t -r -e "ssh -o StrictHostKeyChecking=no" $Output_path/$year/$month/$day/ \
                cctvuser@${Remote_host}:$Remote_path/$year/$month/$day/ && \
                hadoop fs -mkdir -p hdfs://${hdfs_path}/${i}/ && \
                hadoop fs -put ${Output_path}/${year}/${month}/${day}/${save_file}.zip hdfs://${hdfs_path}/${i} && \
                echo "hadoop fs -put hdfs://${hdfs_path}/${i}"
                rm -rf ${Output_path}/${year}/${month}/${day}/${save_file}.zip
                echo "Upload success!" > ${Output_path}/${i}/${save_file}.txt
                echo "`date +%Y/%m/%d_%H:%M:%S`end rsync!"
                echo '======================================================================================================================================================'
        fi
}

function old_targz {
        echo ""
        echo "`date +%Y/%m/%d_%H:%M:%S` begin zip "$Public_path/$year/$month/$day" to "$Output_path/$year/$month/$day/${save_file}.zip
        mkdir -pv $Output_path/$year/$month/$day/ && \
        cd $Public_path/$year/$month/$day && \
                echo "Upload success!" > ${Output_path}/${i}/${save_file}.txt
                echo '======================================================================================================================================================'
}


#  bash -x pushfile_c5data.sh "-2 day" "-1 day" 

if [ ! $1 ] && [ ! $2 ];then
        unix_sdate=$(date -d 19790101 +%s)
        unix_edate=$(date -d `date -d "-60 day" +%Y%m%d` +%s)

else
        date -d "$1" +%s >> /dev/null
        parameter_one=$?
        date -d "$2" +%s >> /dev/null
        parameter_two=$?

        if [ ${parameter_one} -eq 0 ] && [ ${parameter_two} -eq 0 ];then
                unix_sdate=$(date -d "$1" +%s)
                unix_edate=$(date -d "$2" +%s)
        else
                echo "Please enter the correct parameters!"
                exit 1
        fi

fi

cd ${Public_path}
for i in $(find ./ -maxdepth 3  -mindepth 3 | cut -d/ -f2-4|sort )
do
        path_unix_date=$(date -d ${i} +%s) >> /dev/null
        parameter_three=$?
        if [ ${parameter_three} -eq 1 ];then
            echo "Error  ${Public_path}${i}"
            continue
        fi
      
        year=$(echo ${i} | awk -F/ '{print $1}')
        month=$(echo ${i} | awk -F/ '{print $2}')
        day=$(echo ${i} | awk -F/ '{print $3}')
        save_file=$(date -d @${path_unix_date} +%Y%m%d)

        # check file create by start timestamp and end  timestamp

        if [ ${path_unix_date} -ge ${unix_sdate} ] && [ ${path_unix_date} -le ${unix_edate} ];then
                file=$(ls -t ${Public_path}/${i} | head -n 1)
                file_modify_time=`date -d "$(stat ${Public_path}/${i}/${file} | grep "Modify" | cut -d ' ' -f 2)" +%s`
                # upload file 7 days ago
                if [ $[ $(date -d `date +%Y%m%d` +%s) - ${file_modify_time} ] -gt $((24*3600*7)) ];then
                        # check compress by ${save_file}.txt
                        if [   -f ${Output_path}/${i}/${save_file}.txt ];then
                                echo "skiping ${save_file} compression,Because it has been compressed."
                        else   
                                echo "targz"
                                targz
                        fi
                else
                        echo "skiping ${year}-${month}-${day}"
                fi
        fi
done
