from apscheduler.schedulers.background import BlockingScheduler
import time,platform
from datetime import datetime,date

sched = BlockingScheduler()

def job_fun (text = "zach"):
    print("{}\t".format(text),time.ctime())


''''''
# 定时执行
specid = "zach1"
job = sched.add_job(job_fun,'interval',seconds=5,id=specid,coalesce=True,args=[specid,])
job2 = sched.add_job(job_fun,'interval',start_date='2017-06-19 10:42:40' , coalesce=True, seconds=5)


'''
# TODO 计划任务 2017-6-19 10：27：30
job = sched.add_job(job_fun, 'date', run_date=datetime(2017, 6, 19, 10, 27, 30),args=['this is date job'])
'''

'''
# TODO 计划任务 周一到周五21：39执行 2017-6-30开始，2017-9-30停止
job = sched.add_job(job_fun, 'cron', day_of_week='mon-fri', hour=21, minute=39, start_date='2017-06-30' ,end_date='2017-09-30')
'''

#TODO 获得任务属性和状态
sched.print_jobs()
#TODO 获得任务id和执行函数
print(sched.get_jobs())
#TODO 删除任务不执行
#job.remove()
'''
#TODO 暂停以及恢复任务
job2.pause()
job2.resume()
'''
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




