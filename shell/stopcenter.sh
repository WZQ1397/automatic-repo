#!/bin/bash

# 下面需要修改的地方
# 1、HOME=/data/zach根据自己建的目录
# 2、JAVA_HOME=/usr/local/jdk1.7 根据自己JDK的路劲
export HOME=/data/zach
export JAVA_HOME=/usr/local/jdk1.7
export DOMAIN_HOME=${HOME}/domain
export LOG_HOME=${HOME}/logs
export TOMCAT_HOME=${HOME}/server
export CLASSPATH=.:${JAVA_HOME}/lib/dt.jar:${JAVA_HOME}/lib/tools.jar
export PATH=${JAVA_HOME}/bin:${PATH}

#Variable settings begin
# 下面需要修改的地方
# 1、export projectName=center 项目名称，即war包名称
# 2、export serverPort=8001  tomcat本地启动端口，以上面对应
export projectName=center 
export serverPort=8001
#Variable settings end

export JAVA_OPTS="-Dtomcat.server.port=${serverPort}"
export CATALINA_PID="${LOG_HOME}/${projectName}.pid"
export CATALINA_BASE=${DOMAIN_HOME}/${projectName}
${TOMCAT_HOME}/bin/catalina.sh stop 30 -force
exit $?
