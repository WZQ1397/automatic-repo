for list in `ls /etc/glance/glance-*`
do
   cp -rv $list $lisk.bak >> baklog
done