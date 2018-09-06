#!/bin/bash

BACKUP_DIR=/backup/database/
NOW=`date +"%Y-%m-%d"`

IGNORE_COLLECTION_NAMES="
__snapshot__
us.Log
dm.Entity#Recycle
contacts.AddressEntity
portal.Hits
cms.OperationLog"
IGNORE_DB_NAMES="
lenchy-portal
lenchy-lms-new
lenchy-lms-sh
allbrightlaw
"
if [ -d $BACKUP_DIR ]; then
        echo "remove old backups.."
        rm -rf $BACKUP_DIR/*
else
        mkdir -p $BACKUP_DIR
fi


SHOWDBS=`echo -e "show dbs;" |mongo --quiet`
echo $SHOWDBS
DBS=`echo "$SHOWDBS" | awk '{a=$1;for(i=3;i<NF;i+2)a=a FS $i;print a}'`
echo $DBS

for c in $IGNORE_COLLECTION_NAMES
        do
                IGCN="$IGCN --excludeCollection=$c"
        done
for DB in $DBS
do 
 DUMP="yes"
        if [ "$IGNORE_DB_NAMES" != "" ]; then
        for dd in $IGNORE_DB_NAMES 
        do
            if [ $dd == $DB  ]; then
                      echo "ignore $DB"
                      DUMP="no";
            fi
        done
        fi
            if [ $DUMP == "yes" ]; then
                mkdir -p $BACKUP_DIR/$NOW
                mongodump -d $DB $IGCN  --gzip -v -o $BACKUP_DIR/$NOW
            fi

done

echo "done!"
