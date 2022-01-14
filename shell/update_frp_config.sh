start=$1
maxport=$1
pos=`tail -1 current_frp_port.pos`
bash umount.sh
bash mount.sh
if [[ $pos -ne $port ]];
then
   echo "currnet pos is $pos but you input $start:"
   echo -n  "Continue [Y/N]:"
   read choice
   if [[ $choice -ne 'Y' ]] || [[ $choice -ne 'y' ]];
   then
      exit 0
   fi
fi
for path in `df -h | grep zach-bulk-img-disk | awk '{print $NF}'`;
do
  num=`echo $path | awk -F '/' '{print $NF}'`
  port=$(($start+$num))
  if [[ $maxport -lt $port ]];
  then
     maxport=$port
  fi
  echo $port
  sed -i -e 's/box/ydian-frp/g' -e "s/8800/$port/g" $path/etc/frp/frpc.ini
done
echo $maxport >> current_frp_port.pos
echo "========================="
tail -1 current_frp_port.pos
echo "========================="
bash umount.sh

