#logpath=/data/tsjinrong/logs
logpath=$1
bklog=/data/tsjinrong/logrotate
rm -rf $bklog/*
for x in `find $logpath -name "*.gz"` ; 
do
oriname=`echo $x | cut -d / -f 6`
echo $oriname
prefix=`echo $x | cut -d / -f 5`
filename=`echo $logpath/$oriname | sed "s#log.json#$prefix.log.json#g" | sed "s/.gz/.suncash.gz/g" `
mv -bv $logpath/$prefix/$oriname $filename
done
find  $logpath -name *suncash.gz | xargs -i mv {}  $bklog

tar zcvf suncash-`hostname`-`date +%Y%m`-prod.gz $bklog

ossutil64 cp suncash-`hostname`-`date +%Y%m`-prod.gz oss://suncash-logs-backup 
