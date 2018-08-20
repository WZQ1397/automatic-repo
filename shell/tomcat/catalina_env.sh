#!/bin/bash

LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CATALINA_HOME/lib
export LD_LIBRARY_PATH

CATALINA_OPTS="$JAVA_OPTS -Djava.awt.headless=true -XX:+UseNUMA -XX:+UseParallelGC -Xmx18192m -Xms1024m -XX:MaxPermSize=512m -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=9876 -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false"
export CATALINA_OPTS

CATALINA_PID="/var/run/tomcat/tomcat7.pid"
export CATALINA_PID
