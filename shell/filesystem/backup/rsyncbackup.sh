#!/bin/bash
rsync -zrtopg   --progress --delete --password-file=/backup/hanguo/backup.txt   backup@122.144.182.21::web  "/backup/hanguo/$(date +'%Y-%m-%d_%H:%M')_web"
rsync -zrtopg   --progress --delete --password-file=/backup/hanguo/backup.txt   backup@122.144.182.21::mysql   "/backup/hanguo/$(date +'%Y-%m-%d_%H:%M')_mysql"
