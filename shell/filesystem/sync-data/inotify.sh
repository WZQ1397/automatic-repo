#!/bin/bash
Path=/data
ip=$1
sed -ri '/^(.*)inotify.sh$/d' /var/spool/cron/root
/usr/bin/inotifywait -mrq --format '%w%f' -e close_write,deltet $Path | while read file
do
	cd $Path && rsync -az ./ --delete rsync_backup@$ip::backup --password-file=/etc/rsync.password-file
done