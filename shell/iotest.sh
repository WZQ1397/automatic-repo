#!/bin/bash
# author zach.wang
diskname=$1
testname=`basename $diskname`
taskname=$testname$type$blocksize
arg1='-direct=1 -iodepth 1 -thread -rwmixread=70 -ioengine=psync -group_reporting'
percent=4
for blocksize in 4k 8k 16k 32k 4m 8m 16m 32m;
do
    for type in read write randrw;
    do
        echo
        echo "===========" $taskname "============"
        fio -filename=$diskname $arg1 -rw=$type -bs=$blocksize -size=20G -numjobs=30 -runtime=120 -name=$taskname >> $testname.log
        echo "complete " $percent"%"
#       let percent+=4
        percent=`expr $percent + 4`
    done
done
echo "complete " $percent"%"