lsb_functions="/lib/lsb/init-functions"

if test -f $lsb_functions ; 
then
  . $lsb_functions
fi

mysvc()
{
  svc=$1
  log_daemon_msg $svc
  log_progress_msg "starting..."
}
warn()
{
  svc=$1
  mysvc $svc
  log_warning_msg $svc
  log_end_msg 0
}
ok(){
  svc=$1
  mysvc $svc
  log_end_msg 0
}

fail(){
  svc=$1
  mysvc $svc
  log_end_msg 1
}

fail zach
warn zach
