#!/bin/bash
# Author: Zach.Wang

BACKUP_DIR="/data/backup"
if [  ! -d ${BACKUP_DIR} ]; then
	mkdir ${BACKUP_DIR}
fi
NOW=`date +"%Y-%m-%d-%H%M"`

DB_SRC_HOST="127.0.0.1"
DB_NAME="app_data_analysis"

USER="kcl"
PASSWD="tsjrkcl!"

BACKUP_PATH=$BACKUP_DIR/$DB_NAME/$NOW
mkdir -p $BACKUP_PATH
LOG_NAME=$BACKUP_DIR/$DB_NAME/$DB_NAME.log

#backup
BACKUP_CMD="/data/storage/mongo/mongodump"
$BACKUP_CMD -h ${DB_SRC_HOST} -d ${DB_NAME} -o $BACKUP_PATH -u$USER -p ${PASSWD} >>$LOG_NAME  2>&1

[[ $? -eq 0 ]] && echo "BackUp Success!" $NOW >> $LOG_NAME
