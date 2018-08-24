#!/bin/bash  
# AUTHOR: Zach.Wang
# Usage: ./deploy-${WEBAPP_NAME}-${PORT}-${SITE}.sh $URL
# ./deploy-kinesis-parent-10084-sit.sh http://192.168.8.197:10080/job/kinesis-parent-sit/ws/deploy-kinesis/target/kinesis-parent-1.0-SNAPSHOT.jar 

function InitVar()
{
    PARTERN=`echo $0 | awk -F ".sh" '{print $1}'`
    SITE=`echo $PARTERN | awk -F "-" '{print $NF}'`
    PORT=`echo $PARTERN | awk -F "-" '{print $(NF-1)}'`
    
    Count_Split=`echo $PARTERN | grep -o '-' | wc -l`
    WEBAPP_NAME=`echo $PARTERN | awk -F "-" -v num=$Count_Split '{
    for(i=2;i<num;i++)
    {
        printf $i;
        if(i<num-1)
            printf "-";
        else
            print "";
    }}'`
    arr=($SITE $PORT $WEBAPP_NAME)
    echo ${arr[$1]}
}

InitVar $1

SITE=InitVar 0
WEBAPP_NAME=InitVar 2
PORT=InitVar 1

JAR_NAME=${WEBAPP_NAME}-${SITE}.jar
BACK_UP_DIR=/data/backup
DEPLOY_DIR=/data/web/$WEBAPP_NAME-$PORT

MY_JDK=/data/jdk/jdk1.8.0_121/bin/java


KillProgross () {
    PID=`ps aux|grep ${WEBAPP_NAME}|grep -Ev "grep|$0"|awk -F ' ' '{print $2}'`
    kill -9 $PID

}

function BackupJar () {
	NOW=`date +%Y%m%d-%H%M%S`
    mkdir ${BACK_UP_DIR}/${NOW}
    cp ${DEPLOY_DIR}/*.jar  ${BACK_UP_DIR}/${NOW}
}


function GetFile () {
	
	rm -f ${DEPLOY_DIR}/${WEBAPP_NAME}.jar
    cd ${DEPLOY_DIR}
    GIT_URL=$1
    webhook=`echo $GIT_URL | awk -F "://" '{print $2}' | awk -F ":" '{print $1}'`
#    if [[ $SITE -eq "prd" ]]; 
#    then 
#            webhook=192.168.8.197
#    else
#            webhook=172.10.10.13    
#        fi
    curl http://${webhook}:10080/j_acegi_security_check -d "j_username=wget&j_password=Wget123%24%25&from=%2F&json=%7B%22j_username%22%3A+%22wget%22%2C+%22j_password%22%3A+%22Wget123%24%25%22%2C+%22from%22%3A+%22%2F%22%7D&Submit=%E7%99%BB%E5%BD%95" -c cook.test
	curl -O $GIT_URL -b cook.test    

}


function StartUp () {
    cd ${DEPLOY_DIR}
    JAR_PACKAGE=`echo $1 | awk -F "/" '{print $NF}'`
    mv $JAR_PACKAGE $JAR_NAME
    javaArgs="-server -Xms512m -Xmx512m -Xss256k -XX:MetaspaceSize=64m -XX:MaxMetaspaceSize=128m"
    #nohup /data/jdk1.8.0_121/bin/java ${javaArgs} -jar ${JAR_NAME} --spring.profiles.active=${SITE} >>nohup.out 2>&1 &
    nohup $MY_JDK ${javaArgs} -jar ${JAR_NAME}  --server.port=$PORT >>nohup.out 2>&1 &
}

function JarDeploy()
{
    URL=$1
    KillProgross
	if [  ! -d ${DEPLOY_DIR} ]; then
		mkdir ${DEPLOY_DIR}
	else
		echo "${DEPLOY_DIR} exsit!"
	fi
    BackupJar
    GetFile $URL
    StartUp $URL
}

JarDeploy $1
