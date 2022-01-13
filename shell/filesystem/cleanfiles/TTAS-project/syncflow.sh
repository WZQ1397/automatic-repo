#!/bin/bash
function singleton()
{
  name=`basename $0`
  pidpath=/tmp/$name.pid
  if [[ -f "$pidpath" ]];
  then
    kill `cat $pidpath`  
    rm -f $pidpath
  fi
  # only for single process
  #  echo $$ >$pidpath  
  ps aux | grep -v grep | grep $name | awk '{printf $2" "}' | tee $pidpath
  echo "ps aux | grep -v grep | grep $name | awk '{printf \$2\" \"}'"
}

singleton
sleep 30
# kernel optimize 
echo 1024 > /proc/sys/fs/inotify/max_user_instances
echo 100000 > /proc/sys/fs/inotify/max_queued_events
echo 163840 > /proc/sys/fs/inotify/max_user_watches

# global var
BASE_PATH=/var/log/synclogs
mkdir $BASE_PATH
default_src_path=/data2/save-data/camera/movePicFromMemDisk/camera
default_save_path=/data2/save-data/camera
src_path=$1
src_path=${src_path:-default_src_path}
save_path=$2
save_path=${save_path:-default_save_path}
if [[ $2 == "" ]] || [[ $1 == "" ]];
then
   echo "Usage: $0 $src_path $save_path" 
fi

echo "$1" > $BASE_PATH/notify-list

inotifywait -mrq -e close_write,create,attrib,open,close --fromfile $BASE_PATH/notify-list --timefmt '%Y/%m/%d %H:%M' --format '%T %w%f%e' | while read file
do
	rsync -avrzP --delete $src_path $save_path | tee -a $BASE_PATH/sync-`date +%Y-%m-%d`.log
done
