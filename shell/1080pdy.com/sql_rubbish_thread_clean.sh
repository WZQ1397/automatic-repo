#!/bin/bash
if [ ! -n "$format_day" ]; then  
   format_day='%Y%m%d'  
fi  
  
sevendayago=`date -d "-${savedays} day " +${format_day}`

for tmp in {a..z}
do
echo $tmp
mysql -uroot -p12345678 -e "use pdycom_discuz;delete from pre_forum_post where first=0 and message regexp '$$tmp{10,}';"
done
