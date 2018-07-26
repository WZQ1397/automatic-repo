on error resume next
set sysenv=CreateObject("WScript.Shell").Environment("system") '系统环境变量的数组对象
Path = CreateObject("Scripting.FileSystemObject").GetFolder(".").Path
'添加变量
sysenv("PGHOME")="D:\postgresql-9.6.9-1-windows-x64-binaries\pgsql"
sysenv("PGHOST")="localhost"
sysenv("Path")=sysenv("PGHOME")+"\bin;"+sysenv("Path")
sysenv("PGLIB")=sysenv("PGHOME")+"\lib"
sysenv("PGDATA")=sysenv("PGHOME")+"\data"
 
wscript.echo "PostgreSQL环境变量安装成功！不需要重新启动计算机啊！"