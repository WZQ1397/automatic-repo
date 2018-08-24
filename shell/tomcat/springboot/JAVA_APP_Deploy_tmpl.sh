#!/bin/bash  
# AUTHOR: Zach.Wang
# Usage: ./deploy-${WEBAPP_NAME}-${PORT}-${SITE}.sh $URL
# ./deploy-kinesis-parent-10084-sit.sh http://192.168.8.197:10080/job/kinesis-parent-sit/ws/deploy-kinesis/target/kinesis-parent-1.0-SNAPSHOT.jar 


# Collection Var
URL=$1
InitVar $URL

# User Define
DIR_OWNER=web

# Directory Struct Define
WEBAPP_NAME=InitVar 0
PORT=InitVar 1
SITE=InitVar 2

# Universal Directory Define
WEBAPP_DIR=$WEBAPP_NAME-$PORT
ROOT_DIR=/data/web/
BACK_UP_DIR=/data/backup
DEPLOY_DIR=$ROOT_DIR$WEBAPP_DIR

# WAR Package Directory Define
WAR_TMP_DIR=/data/deploy/deploy-$WEBAPP_NAME-$PORT

# Environment Define
ZACH_JAVA=${JAVA_HOME:-/data/jdk/jdk1.8.0_121}
MY_JDK=$ZACH_JAVA/bin/java
echo "Use JDK_PATH: " $MY_JDK

# Split URL Name To Check Deploy Package Type
APP_PACKAGE=`echo $1 | awk -F "/" '{print $NF}'`
APP_SUBFIX=`echo $APP_PACKAGE | cut -d "." -f 2`
APP_NAME=${WEBAPP_NAME}-${SITE}.$APP_SUBFIX
PKG_TYPE=`echo $APP_SUBFIX  | tr '[a-z]' '[A-Z]'`
if [ $PKG_TYPE == WAR ];then
	DEPLOY_DIR=$ROOT_DIR/application/$WEBAPP_NAME-$PORT
fi

: <<'COMMENT'
Get Parameters $WEBAPP_NAME $PORT $SITE From Jenkins Shell Fetch URL
URL from gitbilt
@Para Type
COMMENT
function InitVar(){
	
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
    arr=($WEBAPP_NAME $PORT $SITE)
    echo ${arr[$1]}
}

: <<'COMMENT'
Judge if Package Type is WAR use shutdown.sh
else use kill
COMMENT
function KillProgross () {
	CHECK_TYPE=`ps aux|grep ${WEBAPP_NAME}`
	local Flag=1
	if [ `echo $CHECK_TYPE | grep catalina.startup.Bootstrap | wc -l` -ge 1 ];
	then
		$DEPLOY_DIR/bin/shutdown.sh
		CHECK_TYPE=`ps aux|grep ${WEBAPP_NAME}`
		[[ `echo $CHECK_TYPE | grep catalina.startup.Bootstrap | wc -l` -eq 0 ]] && Flag=0 
	fi
	PID=`echo $CHECK_TYPE | grep -Ev "grep|$0" |awk -F ' ' '{print $2}'`
	echo $PID "KILLED!"
    $Flag && kill -9 $PID
}

: <<'COMMENT'
Backup JAR or WAR Package
COMMENT
function Backup () {
	NOW=`date +%Y%m%d-%H%M%S`
    mkdir -pv ${BACK_UP_DIR}/${NOW}
	test $1 -eq jar && SCOPE=.$APP_SUBFIX || SCOPE=""
    cp -R ${DEPLOY_DIR}/*${SCOPE}  ${BACK_UP_DIR}/${NOW}
	rm -rf ${DEPLOY_DIR}/${WEBAPP_NAME}${SCOPE}
}

: <<'COMMENT'
Download APP PACKAGE From gitbilt URL
Automatic To Judge DEV or PRD Environment
COMMENT
function GetFile () {
	
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
    sleep 2	

}

: <<'COMMENT'
Runing APP 
COMMENT
function StartUp () {
    cd ${DEPLOY_DIR}
    mv $APP_PACKAGE $APP_NAME
	if [ $1 -eq JAR ];then
		JavaArgs="-server -Xms512m -Xmx512m -Xss256k -XX:MetaspaceSize=64m -XX:MaxMetaspaceSize=128m"
		#nohup /data/jdk1.8.0_121/bin/java ${javaArgs} -jar ${JAR_NAME} --spring.profiles.active=${SITE} >>nohup.out 2>&1 &
		nohup $MY_JDK ${JavaArgs} -jar ${APP_NAME}  --server.port=$PORT >>  ${APP_NAME}.log 2>&1 &
	fi
	if [ $1 -eq WAR ];then
		unzip $WAR_TMP_DIR$APP_NAME -d $DEPLOY_DIR
		sleep 2
		local TomcatDir=$ROOT_DIR$WEBAPP_NAME-$PORT
		rm -rf $TomcatDir/work/Catalina/localhost/*
		sleep 2
		$TomcatDir/bin/startup.sh
		sleep 15
		tail -150  $TomcatDir/logs/catalina.out
	fi
}

function CheckDirExists(){
	local Dir
	if [  ! -d $Dir ]; then
		mkdir $Dir
		chown -R $DIR_OWNER.$DIR_OWNER $Dir
		echo "$Dir Created! Owner "$DIR_OWNER
	else
		echo "$Dir Exsit!"
	fi
}

function CheckUserExists(){
	id $DIR_OWNER >> /dev/null 2>&1
	if [ $? -nq 0 ];then
		echo "User " $DIR_OWNER "Not Exists!"
		useradd $DIR_OWNER
		echo "User " $DIR_OWNER "Created!"
	else
		echo "User " $DIR_OWNER "is OK!"
	fi
}

function InitEnv(){
    KillProgross
	CheckUserExists
	if [ $1 == WAR ];then
		local DirLst=(ROOT_DIR BACK_UP_DIR DEPLOY_DIR WAR_TMP_DIR)
	else
		local DirLst=(ROOT_DIR BACK_UP_DIR DEPLOY_DIR)
	fi
	for KEY_WORD in DirLst
	do
		CheckDirExists $KEY_WORD
	done	
}

: <<'COMMENT'
This is Main function Don`t Change it!
COMMENT
function Deploy(){
	local Type=$2
	InitEnv $Type
    Backup $Type
    GetFile $URL
    StartUp $Type
}

# Main function Start
Deploy $URL $PKG_TYPE

