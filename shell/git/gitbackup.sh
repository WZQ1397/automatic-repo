#!/bin/bash
back_num=`docker exec -t gitlab_web_1 bash -c "ls /var/opt/gitlab/backups/*gitlab_backup.tar" | wc -l`

function backup {
	docker exec -t gitlab_web_1 gitlab-rake gitlab:backup:create
}

if [ ${back_num} -ge 3 ];then
	redundancy=`docker exec -t gitlab_web_1 bash -c "ls -t /var/opt/gitlab/backups/*gitlab_backup.tar | tail -n1"`
	docker exec -t gitlab_web_1 rm -rf ${redundancy}
	backup
else
	backup
fi
