@echo off
set PATH=%PATH%;D:\works\repository\rsync_edong\bin

set OPT=-vrtz --delete -e "ssh -p 698"
set SKIP=--exclude .git --exclude *.spec --exclude .gitignore --exclude '*.cmd'

set SRC=/cygdrive/h/works/saltstack/config/
set DST=root@salt.tonyc.cn:/srv/

rem for /F %%i in ('cygpath.exe -w %SRC%' ) do set worktree=%%i

rem for /F %%i in ('git --git-dir=%worktree%\.git rev-parse --abbrev-ref HEAD') do set branch=%%i

rem if "%branch%"=="master" set branch=base

rsync  %OPT% %SKIP% %DST% %SRC% 

rem --exclude prod/states/dns
rem rsync %OPT% %SKIP% %DST%/prod/states/dns/ %SRC%/prod/states/dns/ 