from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from pymongo import MongoClient
from apscheduler.executors.pool import ThreadPoolExecutor,ProcessPoolExecutor
import time

host = '127.0.0.1'
port = '27017'

def job_fun (text = "zach"):
    print("{}\t".format(text),time.ctime())

#sched = BlockingScheduler(jobstores=jobstores,executors=executors,job_defaults=job_defaults)
# 简单执行
sched = BlockingScheduler()
client = MongoClient(host=host,port=port)
storge = MongoDBJobStore(client=client)
sched.add_jobstore(storge)
# 定时执行
specid = "zach1"
job = sched.add_job(job_fun,'interval',seconds=5,id=specid,args=[specid,])
job2 = sched.add_job(job_fun,'interval',start_date='2017-06-19 10:42:40' , seconds=5)

job.modify(max_instances=6, name='Alternate name')
sched.start()