#!/bin/bash
# sync the whole database
BACKUP_DIR="/data/backup"
NOW=`date +"%Y-%m-%d-%H%M"`

DB_SRC_HOST="192.168.10.14"
DB_SRC_NAME="lenchy-bar-sd"

DB_DES_HOST="10.10.2.112"
DB_DES_NAME="lenchy-bar"

BACKUP_PATH=$BACKUP_DIR/$DB_SRC_NAME/$NOW
TEMP_PATH=/tmp/$DB_SRC_NAME/$NOW
mkdir -p $BACKUP_PATH

#do backup
mongodump -h $DB_DES_HOST -d $DB_DES_NAME -o $BACKUP_PATH

#do dump to temp dir
mongodump -h $DB_SRC_HOST -d $DB_SRC_NAME -o $TEMP_PATH

#do override to the dest database.
mongorestore -d $DB_DES_NAME -h $DB_DES_HOST --drop $TEMP_PATH/$DB_SRC_NAME

rm -rf $TEMP_PATH
