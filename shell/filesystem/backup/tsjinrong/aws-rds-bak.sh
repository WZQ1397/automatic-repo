#!/bin/bash
DATE=`date "+%Y%m%d%H%M%S"`
# crontab: 30 01 * * * /data/script/aws-rds-bak.sh >> /tmp/rds-bak.logs
#back-cli
#sit
#aws rds create-db-snapshot --db-snapshot-identifier mysql-sit-back-$DATE --db-instance-identifier mysql-sit
#sleep 20
#prd01
/usr/local/bin/aws rds create-db-snapshot --db-snapshot-identifier inside-prd01-back-$DATE --db-instance-identifier inside-prd01
