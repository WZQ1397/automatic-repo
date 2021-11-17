target_root=/zach-ramdisk/data/static/heartmap
reserve_file_nums=200
tmp_dir=/tmp/cam-data
mkdir -pv $tmp_dir

while true;
do
  for cam in `seq 1 9`;
  do
    total=$(ls $target_root/$cam/ | wc -l)
    ind=$(($total-$reserve_file_nums))
    if [[ $ind -le $reserve_file_nums ]];
    then
      continue
    fi
    #list=(`ls $target_root/$cam/* | tail -$ind`)
    list=(`find $target_root/$cam/ | tail -$ind`)
    echo ${#list[@]}
    for x in ${list[@]};
    do
      #echo $x;
      mv -v $x /tmp/cam-data
      if [[ ${#list[@]} -le $reserve_file_nums ]];
      then
        break
      fi
    done
  done
  rm -rvf  $tmp_dir/*
  sleep 30
done
