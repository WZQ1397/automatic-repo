#!/bin/bash

BACKUP_DIR="/data/backup"
NOW=`date +"%Y-%m-%d-%H%M"`

DB_SRC_HOST="192.168.10.14"
DB_SRC_NAME="lenchy-bar-sd"

DB_DES_HOST="10.10.2.112"
DB_DES_NAME="lenchy-bar"


COLLECTIONS="
dm.Action
dm.Business
dm.DataType
dm.Field
dm.Listener
dm.Macro
dm.Module
dm.Renderer
dm.Schedule
dm.Servlet
dm.Type
dm.View
"
BACKUP_PATH=$BACKUP_DIR/$DB_SRC_NAME/$NOW
TEMP_PATH=/tmp/$DB_SRC_NAME/$NOW
mkdir -p $BACKUP_PATH

#do backup
for c in $COLLECTIONS
do
   mongodump -h $DB_DES_HOST -d $DB_DES_NAME -o $BACKUP_PATH -c $c
done

#do dump to temp dir
for c in $COLLECTIONS
do
   mongodump -h $DB_SRC_HOST -d $DB_SRC_NAME -o $TEMP_PATH -c $c
done

#do override to the dest database.
mongorestore -d $DB_DES_NAME -h $DB_DES_HOST --drop $TEMP_PATH/$DB_SRC_NAME

rm -rf $TEMP_PATH
