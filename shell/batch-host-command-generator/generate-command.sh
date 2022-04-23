#!/bin/bash
# Author: Zach.Wang
# DESC: generate auto run command


CONDITION=$1
CONDITION=${CONDITION:-*}
EXEC_COMMAND="$2"
[[ -z $EXEC_COMMAND ]] && exit


. ./get_host_list_from_puppetdb.sh
get_host_list $CONDITION

CMD="sshpass -f keyfile ssh  -o ConnectTimeout=3 -o ConnectionAttempts=5 -o StrictHostKeyChecking=no"
generate_res_path=filter-$CONDITION-`date +%Y-%m-%d`-res
generate_host_list=filter-$CONDITION-`date +%Y-%m-%d`.log
mkdir -pv $generate_res_path
> command.log
while read host
do
    echo "$CMD $host \"$EXEC_COMMAND\" > $generate_res_path/$host" | tee -a command.log
    echo "======================================"
    # $CMD $host \"$EXEC_COMMAND\" >> $generate_host_list.exec.result
done < $generate_host_list
