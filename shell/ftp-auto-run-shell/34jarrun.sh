BASEPATH="/home/cctvuser/src/bin/area/sparksteamming/2021-07_area_userdata_etl/"
RUNNER_SHELL="zrun.sh"
JAR_PKG_PATH="target"
pd="1234"
ip=34
JAR_NAME="cctv_area_userdata_etl-1.0-SNAPSHOT-jar-with-dependencies.jar"
/usr/bin/sshpass -p $pd  scp -o StrictHostKeyChecking=no /home/ftpdir/pkg/34/$JAR_NAME $BASEPATH/$JAR_PKG_PATH
/usr/bin/sshpass -p $pd  ssh -o StrictHostKeyChecking=no cctvuser@10.110.142.$ip $BASEPATH/$RUNNER_SHELL
