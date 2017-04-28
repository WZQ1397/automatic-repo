@echo off
echo.
echo data syncing...
echo.
cd C:\Program Files (x86)\rsync\bin
rsync -vzrtopg --ignore-errors --progress --password-file="/cygdrive/c/rsync.password" --exclude={"*Log*","*log"} SvcCWRSYNC@192.168.36.21::project /cygdrive/e/project/backup
echo.
echo sync completed
echo.