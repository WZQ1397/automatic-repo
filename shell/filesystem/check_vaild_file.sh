#!/bin/bash
function check_size(){
  meta_info_size=`curl -s -I 6.6.6.6:8081/job/app-sit/1342/execution/node/3/ws/target/app-0.0.1-SNAPSHOT.jar | grep Content-Length | cut -d ' ' -f 2 | sed 's/\r//g'` 
  current_size=`du -b /tsjr-data/deploy-java/tsjr-app-sit-8080.jar | awk '{print $1}'`
  echo "ori:" $meta_info_size
  echo "current:" $current_size
  if [[ $meta_info_size -eq $current_size ]]
  then
    echo "ok"
  else
   echo "broken"
   exit 255
  fi
}
