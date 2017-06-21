from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import (EVENT_JOB_EXECUTED,EVENT_JOB_ERROR,EVENT_JOB_MISSED)
import time,platform
#后台执行
sched = BackgroundScheduler()

def job_fun (text = "zach"):
    print("{}\t".format(text),time.ctime())

#监听器
def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')
''''''
# 定时执行
specid = "zach1"
job = sched.add_job(job_fun,'interval',seconds=5,id=specid,coalesce=True,args=[specid,])
job2 = sched.add_job(job_fun,'interval',start_date='2017-06-19 10:42:40' , coalesce=True, seconds=5)
#添加监听器和监听状态
sched.add_listener(my_listener,EVENT_JOB_EXECUTED|EVENT_JOB_ERROR|EVENT_JOB_MISSED)
print("press Ctrl+{} TO STOP TASK".format('break' if platform.system() == 'Windows' else 'C'))
try:
    sched.start()
except (SyntaxWarning,BlockingIOError,SystemError) as e:
    print(e)
except (KeyboardInterrupt,SystemExit):
    print('clean the job')
    #TODO 获得任务id和执行函数
    print(sched.get_jobs())
    taskid = str(input('input id'))
    sched.remove_job(taskid)
    if taskid.isspace() or taskid.isidentifier():
        sched.remove_all_jobs()




