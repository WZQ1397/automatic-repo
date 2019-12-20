list=()
first=42
last=72
for x in `seq $first $last`; 
do
 indice=$(date --date "$x days ago" +%Y.%m.%d)
 if [[ $x -eq $last ]];
 then
   list[x]=\"logstash-$indice\"
 else
   list[x]=\"logstash-$indice\",
 fi
done
echo " 
curl -X POST 'http://47.74.219.229:29200/_reindex' -H 'Content-Type: application/json' -d'
{
\"source\": {
\"index\": [${list[@]}]
},
\"dest\": {
\"index\": \"logstash-2019.10-full\"
}
}'
"
