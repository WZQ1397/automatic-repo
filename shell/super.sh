checkProcess(){
   pid=`ps -ef|grep ${classname}|grep -v 'grep'|awk '{print $2}'`
   if [ "X${pid}" != "X" ]; then
      return 0
   else
      return 1
   fi
}

printStartStatus(){
   checkProcess
   if [ $? -eq 0 ]; then
      echo "${_moduleName} start sucessful.      [OK]"
      return 0
   else
      echo "${_moduleName} start Failed.      [Failed]"
      return 1
   fi
}

startProcess(){
   echo $1
   checkProcess
   if [ $? -eq 0 ]; then
          echo "${_moduleName} had started."
      return 0
   else
      ${start}
      sleep 3 
          printStartStatus
   fi       
}

stopProcess(){
   echo $1
   checkProcess
   if [ $? -eq 1 ]; then
      echo "${_moduleName} not running.      [FAILED]"
   else
      pid=`ps -ef|grep ${classname}|grep -v 'grep'|awk '{print $2}'`
      if [ "X${pid}" = "X" ]; then
          echo "${_moduleName} had stop.       [OK]"
      else
          kill -9 $pid
          echo "${_moduleName} stop sucessful.       [OK]"
      fi
   fi
}

restartProcess(){
   stopProcess $1
   startProcess $2
}

getProcessStatus(){
   checkProcess
   if [ $? -eq 0 ]; then
      echo "${_moduleName} is running."
      return 0
   else
      echo "${_moduleName} is not running."
      return 1
   fi
}

unstall(){
   checkProcess
   if [ $? -eq 0 ]; then
      pid=`ps -ef|grep ${classname}|grep -v 'grep'|awk '{print $2}'`
      if [ "X${pid}" != "X" ]; then
         kill -9 $pid
      fi
   fi
   ${remove}
}

commandError(){
   echo ""
   echo "ERROR:UNKNOWN COMMAND:\"$_command\" "
   exit 1
}
