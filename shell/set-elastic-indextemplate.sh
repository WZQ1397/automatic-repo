#!/usr/bin/env bash

#get all node load info
#curl 'localhost:9200/_cat/nodes?v'

#get template('logstash') info
#curl -XGET 'localhost:9200/_template/logstash?pretty'

#get all indices
#curl 'localhost:9200/_cat/indices?v'

#get one index(logstash-2015.07.28) settings
#curl -XGET 'localhost:9200/logstash-2015.07.28/_settings?pretty'

#delete one index template(template_1)
#curl -XDELETE localhost:9200/_template/template_1

#check indices health statistics.
#curl -XGET 'http://localhost:9200/_cluster/health?level=indices' | python -m json.tool

#get indices routing table nodes info.
#curl -XGET "http://localhost:9200/_cluster/state/routing_table,routing_nodes/kibana-int-yongning" | python -m json.tool

#delete one index.
#curl -XDELETE http://localhost:9200/.marvel-2016.02.19

curl -XPUT localhost:9200/_template/base -d '
{
  "order": 1,
  "template" : "logstash-*",
  "settings": {
    "index.refresh_interval": "30s",
    "index.number_of_replicas": "1",
    "index.number_of_shards": "8",
    "index.routing.allocation.total_shards_per_node": "2",
    "index.search.slowlog.threshold.query.warn": "10s",
    "index.search.slowlog.threshold.query.info": "5s",
    "index.search.slowlog.threshold.fetch.warn": "1s",
    "index.search.slowlog.threshold.fetch.info": "800ms",
    "index.indexing.slowlog.threshold.index.warn": "10s",
    "index.indexing.slowlog.threshold.index.info": "5s"
  },
  "mappings": {
    "_default_": {
      "dynamic_templates": [
        {
          "integer field": {
            "mapping": {
              "doc_values": true,
              "type": "integer"
            },
            "match": "*",
            "match_mapping_type": "integer"
          }
        },
        {
          "date field": {
            "mapping": {
              "doc_values": true,
              "type": "date"
            },
            "match": "*",
            "match_mapping_type": "date"
          }
        },
        {
          "long field": {
            "mapping": {
              "doc_values": true,
              "type": "long"
            },
            "match": "*",
            "match_mapping_type": "long"
          }
        },
        {
          "float field": {
            "mapping": {
              "doc_values": true,
              "type": "float"
            },
            "match": "*",
            "match_mapping_type": "float"
          }
        },
        {
          "double field": {
            "mapping": {
              "doc_values": true,
              "type": "double"
            },
            "match": "*",
            "match_mapping_type": "double"
          }
        },
        {
          "byte field": {
            "mapping": {
              "doc_values": true,
              "type": "byte"
            },
            "match": "*",
            "match_mapping_type": "byte"
          }
        },
        {
          "short field": {
            "mapping": {
              "doc_values": true,
              "type": "short"
            },
            "match": "*",
            "match_mapping_type": "short"
          }
        },
        {
          "binary field": {
            "mapping": {
              "doc_values": true,
              "type": "binary"
            },
            "match": "*",
            "match_mapping_type": "binary"
          }
        },
        {
          "geo_point field": {
            "mapping": {
              "doc_values": true,
              "type": "geo_point"
            },
            "match": "*",
            "match_mapping_type": "geo_point"
          }
        },
        {
          "string_fields": {
            "mapping": {
              "index": "not_analyzed",
              "omit_norms": true,
              "doc_values": true,
              "type": "string",
              "fields" : {
                "raw" : {
                  "index" : "not_analyzed",
                  "ignore_above" : 256,
                  "type" : "string"
                }
              }
            },
            "match": "*",
            "match_mapping_type": "string"
          }
        }
      ],
      "_all": {
        "enabled": true
      }
    }
  }
}
'

curl -XPUT localhost:9200/_template/kibana-int -d '
{
  "order": 1,
  "template" : "kibana-int-*",
  "settings": {
    "index.number_of_replicas": "1",
    "index.number_of_shards": "1",
    "index.search.slowlog.threshold.query.warn": "10s",
    "index.search.slowlog.threshold.query.info": "5s",
    "index.search.slowlog.threshold.fetch.warn": "1s",
    "index.search.slowlog.threshold.fetch.info": "800ms",
    "index.indexing.slowlog.threshold.index.warn": "10s",
    "index.indexing.slowlog.threshold.index.info": "5s"
  }
}
'