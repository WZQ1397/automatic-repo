echo "port = 3726 " >> /etc/my.cnf
mysql -u root -pRC%*rc170718
use mysql;
update user set authentication_string=password("d2eda447a86c") where user="root";
flush privileges;
\q;

systemctl stop mysqld
systemctl start mysqld
systemctl status mysqld
