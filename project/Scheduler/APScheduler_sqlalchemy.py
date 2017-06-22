from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor,ProcessPoolExecutor
import time
from datetime import datetime,date

# 使用sqlite存储作业
sqlitedb = r"E:\\sqlitedb1.db"
url = r'sqlite:///%s' %sqlitedb

# 使用mysql存储作业
# url = 'mysql://root:123456@localhost/Sched'

#TODO 模版区域
jobstores = {
    'default': SQLAlchemyJobStore(url=url)
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

def job_fun (text = "zach"):
    print("{}\t".format(text),time.ctime())

#sched = BlockingScheduler(jobstores=jobstores,executors=executors,job_defaults=job_defaults)
# 简单执行
sched = BlockingScheduler()
sched.add_jobstore('sqlalchemy',url=url)
# 定时执行
specid = "zach1"
job = sched.add_job(job_fun,'interval',seconds=5,id=specid,args=[specid,])
job2 = sched.add_job(job_fun,'interval',start_date='2017-06-19 10:42:40' , seconds=5)

sched.start()