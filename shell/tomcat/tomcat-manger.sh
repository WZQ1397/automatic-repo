#!/bin/sh

# 下面需要修改的地方
# 1、classname="tjtag=center" center服务名称
# 2、_moduleName="center" modul名称
# 3、start="/data/zach/sbin/startcenter.sh" 上面新建的脚本
# 4、. /data/zach/sbin/super.sh 上面新建的脚本
classname="tjtag=center" 
_command=$1
_moduleName="center"
start="/data/zach/sbin/startcenter.sh"
. /data/zach/sbin/super.sh
case $_command in
   start)
      startProcess "Starting ${_moduldName}:"
   ;;
   stop)
      stopProcess "Stoping ${_moduldName}:"
   ;;
   restart)
      restartProcess "Stoping ${_moduldName}:" "Starting ${_moduldName}:"
   ;;
   status)
      getProcessStatus
   ;;
   unstall)
      unstall
   ;;
 *)
   commandError
 ;;
esac
