#!/bin/bash

for index in $(curl  -s 'http://172.16.48.66:9200/_cat/shards' | grep UNASSIGNED | awk '{print $1}' | sort | uniq); do
    for shard in $(curl  -s 'http://172.16.48.66:9200/_cat/shards' | grep UNASSIGNED | grep $index | awk '{print $2}' | sort | uniq); do
        echo  $index $shard

        curl -XPOST '172.16.48.66:9200/_cluster/reroute' -d '{
            "commands" : [ {
                  "allocate" : {
                      "index" : logstash-2017.12.04,
                      "shard" : 0,
                      "node" : 'Master',
                      "allow_primary" : true
                  }
                }
            ]
        }'

        sleep 5
    done
done
