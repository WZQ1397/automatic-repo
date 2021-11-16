target_root=/zach-ramdisk/data/static/heartmap
reserve_file_nums=100
cd $target_root
while true;
do
  for cam in `seq 1 9`;
  do
    ls -t $target_root/$cam/ | awk "NR>$reserve_file_nums{print $1}" | xargs rm -rvf {};
  done
done
