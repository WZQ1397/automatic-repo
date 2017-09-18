for tmp in {a..z}
do
echo $tmp
mysql -uroot -p12345678 -e "use pdycom_discuz;delete from pre_forum_post where first=0 and message regexp  '$tmp{10,}' ;"
done
