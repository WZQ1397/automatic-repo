#!/bin/bash
SRC_URL="http://localhost:9200/"
SRC_PATH=""
SRC_INDEX_NAME="logstash-$(date +%Y.%m.%d)"
SRC_CONTENT="$SRC_URL$SRC_PATH$SRC_INDEX_NAME"
DST_URL=""
DST_PATH="/data/es-bak/"
DST_INDEX_NAME=""

function usage(){
cat <<EOF
###########################################################
#  Author     : zach.wang                                 #
###########################################################
Usage: $0 [OPTION]... [-b|-r]
       -u SRC_URL source elasticsearch cluster url 
	      Default: $SRC_URL
       -U DST_URL destination elasticsearch cluster url
	      Default: $SRC_URL
       -i SRC_INDEX_NAME source backup elasticsearch index name 
	      Default: $SRC_INDEX_NAME
       -I DST_INDEX_NAME destination output elasticsearch index name
	      Default: $SRC_INDEX_NAME
       -p SRC_PATH source dump file path
       -P DST_PATH destination dump file path
	      Default: $DST_PATH
     Final option (This is the Must!)
       -b create dump for elasticsearch
       -r recover dump file to elasticsearch
	   
Example: backup elasticsearch to dump file
         $0 -u http://172.16.48.102:9200/ -i .monitoring-kibana-6-2019.09.10 -b
EOF
}

function check_vaild()
{
  if [[ $SRC_URL != $SRC_PATH ]];then
    if [[ -z $SRC_URL ]];then
      if [[ -z $SRC_PATH ]];then
        echo "please input SRC_PATH!"
        exit 255
      fi
    else
      if [[ ! -z $SRC_PATH ]];then
        echo "SRC_URL cannot use SRC_PATH together!"
        exit 255
      fi
    fi
    echo "source syntax check ok"
  fi
  if [[ $DST_URL != $DST_PATH ]];then
    if [[ -z $DST_URL ]];then
      if [[ -z $DST_PATH ]];then
        echo "please input DST_PATH!"
        exit 255
      fi
    else
      if [[ ! -z $DST_PATH ]];then
        echo "DST_URL cannot use DST_PATH together!"
        exit 255
      fi
    fi
    echo "destination syntax check ok"
  fi
  return 0
}

function dump()
{
  SRC_CONTENT="$SRC_URL$SRC_PATH$SRC_INDEX_NAME"
  if [[ check_vaild -eq 0 ]];
  then
    if [[ $DST_INDEX_NAME == "" ]];then
      DST_INDEX_NAME=$SRC_INDEX_NAME
    fi
    DST_CONTENT="$DST_URL$DST_PATH$DST_INDEX_NAME"
    echo "Backuping: $SRC_CONTENT --> $DST_CONTENT"
    docker run --rm -ti -v $DST_PATH:$DST_PATH taskrabbit/elasticsearch-dump --input=$SRC_CONTENT --output=$ --limit=10000 | gzip > $DST_CONTENT.gz
  fi
}

function recover()
{
  if [[ check_vaild -eq 0 ]];
  then
    SRC_CONTENT="$SRC_PATH$SRC_INDEX_NAME"
    if [[ ! -f $SRC_CONTENT.gz ]];then
      echo "Recovering failed: $SRC_CONTENT.gz not exists!"
	  exit 255
    fi
	if [[ $DST_INDEX_NAME == "" ]];then
      DST_INDEX_NAME=$SRC_INDEX_NAME
    fi
	DST_CONTENT="$DST_URL$DST_INDEX_NAME"
    echo "Recovering: $SRC_CONTENT --> $DST_CONTENT"
	gzip -d $SRC_CONTENT.gz
    docker run --rm -ti -v $SRC_PATH:$SRC_PATH taskrabbit/elasticsearch-dump --input=$SRC_CONTENT --output=$DST_CONTENT --limit=10000
  fi
}

while getopts :u:U:i:I:p:P:br:h opt
do
  case $opt in
  u) SRC_URL=$OPTARG;;
  U) DST_URL=$OPTARG;;
  i) SRC_INDEX_NAME=$OPTARG;;
  I) DST_INDEX_NAME=$OPTARG;;
  p) SRC_PATH=$OPTARG;;
  P) DST_PATH=$OPTARG;;
  h) usage ;;
  b) dump;;
  r) recover;;
  *) usage ;;
  esac
done
