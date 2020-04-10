JAVA_HOME=/MyCAT/jdk/jdk1.7.0_79
JRE_HOME=/MyCAT/jdk/jdk1.7.0_79/jre
MAVEN_HOME=/usr/local/apache-maven
export MAVEN_HOME
export JAVA_HOME
export JRE_HOME
export PATH=${PATH}:${MAVEN_HOME}/bin:${JAVA_HOME}:${JRE_HOME}
export JAVA_OPTS="$JAVA_OPTS -server -Xmn512m -Xms512m -Xmx1024m -XX:MaxNewSize=512m -XX:PermSize=512m -XX:MaxPermSize=512m -verbose:gc -XX:+PrintGC -XX:+PrintGCDetails -XX:+PrintTenuringDistribution -XX:+PrintHeapAtGC -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps -XX:+
HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/data/web -Xloggc:/data/web/collectionweb_gc.log"