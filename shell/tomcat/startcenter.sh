#!/bin/bash

# 下面需要修改的地方
# 1、HOME=/data/zach根据自己建的目录
export HOME=/data/zach
export DOMAIN_HOME=${HOME}/domain
export LOG_HOME=${HOME}/logs
export TOMCAT_HOME=${HOME}/server

#Variable settings begin
# 下面需要修改的地方
# 1、export projectName=center  服务名称，即war包名称
# 2、export httpPort=7001  启动接收请求端口端口
# 3、export serverPort=8001  tomcat启动的本地端口
export projectName=center
export httpPort=7001
export serverPort=8001
export minMsMem=3200m
export maxMsMem=3200m
export ssMem=300k
export mnMem=1100m
export survivorRatior=2
export minPermSize=250m
export maxPermSize=300m
export threshold=20
export fraction=60
export pageSize=128m
export warFile=${HOME}/center_webapps # 服务名加webapps war包地址
export logFile=${LOG_HOME}/${projectName}/catalina.$(date +'%Y-%m-%d').out
export pidFile=${LOG_HOME}/${projectName}.pid
export LD_LIBRARY_PATH=/usr/local/apr/lib
export heapDumpPath=${DOMAIN_HOME}/${projectName}/heapDump
#Variable settings end

#JVM args settings begin
# 下面需要修改的地方：
# 1、Dtjtag=center服务名称
CATALINA_OPTS="-server -Dtjtag=center -Dtomcat.server.port=${serverPort} -Dtomcat.http.port=${httpPort} -Dtomcat.deploy.home=${warFile}"
CATALINA_OPTS="${CATALINA_OPTS} -Xms${minMsMem} -Xmx${maxMsMem} -Xss${ssMem} -Xmn${mnMem} -XX:SurvivorRatio=${survivorRatior} -XX:PermSize=${minPermSize} -XX:MaxPermSize=${maxPermSize}"
CATALINA_OPTS="${CATALINA_OPTS} -XX:+UseCompressedOops -XX:+TieredCompilation -XX:+AggressiveOpts -XX:+UseBiasedLocking"
CATALINA_OPTS="${CATALINA_OPTS} -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -Xnoclassgc -XX:MaxTenuringThreshold=${threshold} -XX:CMSInitiatingOccupancyFraction=${fraction} -XX:LargePageSizeInBytes=${pageSize} -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=${heapDumpPath}"
#JVM args settings end

export CATALINA_BASE=${DOMAIN_HOME}/${projectName}
export CATALINA_OPTS
export CATALINA_OUT="${logFile}"
export CATALINA_PID="${pidFile}"
export CATALINA_OPTS
${TOMCAT_HOME}/bin/catalina.sh start
