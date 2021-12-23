dirname=filter-data-`date +%Y-%m-%d`
mkdir -pv $dirname/./{1..9}
while read DATE TIME
do
  timestamp=`date +%s -d "$DATE $TIME"`
  echo $timestamp
  find . -name "$timestamp*" -type d
  length=$((${#timestamp}-2))
  widetimestamp=${timestamp:0:$length}
  echo "Wide Search: $widetimestamp"
  find . -name "$widetimestamp*" -type d  | xargs -i cp -rv {} $dirname/{}  
  # exit
done < timelist.conf
sshpass -p zach rsync -avzP -e "ssh -p 2222" $dirname zach@202.0.9.2:/DATA9_DB12/return-data/content-data/ttas/online-data
