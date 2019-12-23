first=42
last=72
for x in `seq $first $last`;
do
 indice=$(date --date "$x days ago" +%Y.%m.%d)
 curl -X POST "http://47.74.219.229:29200/logstash-$indice/_delete_by_query?wait_for_completion=false" -H 'Content-Type: application/json' -d'
{
    "query": {
        "bool": {
          "should":[
            {"term":{"profile": "sit"}},
            {"term":{"tag": "kubelet"}},
            {"term":{"severity": "DEBUG"}}
            ]
        }
    }
}
'
done
