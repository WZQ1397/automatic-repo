1.同步时间
ntpdate ntp2.aliyun.com

2. 修改 /etc/hosts
mv /etc/hosts /etc/hosts.bk
cat >> /etc/hosts << EOF
172.16.10.111   rabbitmq1
172.16.10.120   rabbitmq2
172.16.10.117   rabbitmq3
EOF

3.安装 erlang、rabbitmq
apt-get update
apt-get install erlang rabbitmq-server -y

4.修改配置
chmod 777 /etc/rabbitmq/
rabbitmqctl stop
/etc/init.d/rabbitmq-server start
rabbitmq-plugins enable rabbitmq_management
netstat -tnlp|grep 15672
rabbitmqctl add_user root 123456
rabbitmqctl set_user_tags root administrator
rabbitmqctl set_permissions -p / root ".*" ".*" ".*"

5.设置 Erlang Cookie
scp /var/lib/rabbitmq/.erlang.cookie root@172.16.10.120:/var/lib/rabbitmq/.erlang.cookie
scp /var/lib/rabbitmq/.erlang.cookie root@172.16.10.120:/var/lib/rabbitmq/.erlang.cookie
rabbitmqctl stop
rabbitmq-server -detached

6.组成集群
rabbitmqctl stop_app 
rabbitmqctl join_cluster rabbit@rabbitmq1
rabbitmqctl start_app
