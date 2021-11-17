target_root=/zach-ramdisk/data/static/heartmap
reserve_file_nums=100
cd $target_root
while true;
do
  for cam in `seq 1 9`;
  do
     find $target_root/$cam/ | awk 'NR>100{print $1}' | xargs rm -rvf {};
  done
  sleep 30
done
