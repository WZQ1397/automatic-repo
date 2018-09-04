#!/bin/bash
#!/bin/bash
# Author: Zach.Wang
DB_SRC_HOST=""
DB_NAME=""
USER=""
PASSWD=""

for KEY_WORD in DB_SRC_HOST DB_NAME USER PASSWD BACKUP_CMD BACKUP_DIR
do
  eval $KEY_WORD=`grep -m1 $KEY_WORD MongoBackup.sh | awk -F "=" '{printf $2}'`
done

#echo $DB_SRC_HOST $DB_NAME $USER $PASSWD
last=ll -t | egrep -v "*.log" | head -2 | tail -1 | awk '{print $NF}'

$BACKUP_CMD/mongorestore -d $DB_NAME -h $DB_SRC_HOST -u$USER -p$PASSWD $BACKUP_DIR/$DB_NAME/$last/$DB_NAME
