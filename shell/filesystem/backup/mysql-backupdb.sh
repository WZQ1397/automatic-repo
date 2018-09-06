#!/bin/bash

# homolo mysql backup

MYSQL_USER="root"
MYSQL_PASS="3116"
MYSQL_PORT="3306"
MYSQL_HOST="127.0.0.1"

IGNORE_DBS="
information_schema
mysql
test
"

ROOT_UID=0
E_NOTROOT=67
if [ "$UID" -ne "$ROOT_UID" ]
then
    echo "Must be root to run this script."
    exit $E_NOTROOT
fi

BACKUP_DIR=/backup/database
if [ -d $BACKUP_DIR ]; then
        echo "remove old backups.."
        rm -rf $BACKUP_DIR/*
else
        mkdir -p $BACKUP_DIR
fi

curdir="$(pwd)"

NOW=`date +"%Y-%m-%d-%H%M"`

MYSQL=`which mysql`;
MYSQLDUMP=`which mysqldump`;
GZIP=`which gzip`;

DBS="$($MYSQL -u $MYSQL_USER -p$MYSQL_PASS -h $MYSQL_HOST -P $MYSQL_PORT -Bse 'show databases')"

for db in $DBS
do
        DUMP_DB="yes";
        if [ "$IGNORE_DBS" != "" ]; then
                for k in $IGNORE_DBS # Store all value of $IGNOREDB ON i
                do
                        if [ "$db" == "$k" ]; then
                                DUMP_DB="NO";
                        fi
                done
        fi

        if [ "$DUMP_DB" == "yes" ]; then # If value of DUMP is "yes" then backup database
            FILE="$BACKUP_DIR/$db-$NOW.gz";
            echo "backing up database $db";
            $MYSQLDUMP --add-drop-database --opt --lock-all-tables -u $MYSQL_USER -p$MYSQL_PASS -h $MYSQL_HOST -P $MYSQL_PORT $db | $GZIP > $FILE
        fi
done
echo "backup done."
