import psutil,datetime,time
from psutil import Popen
print("\n"+"CPU部分".center(50,'-'))
print(psutil.cpu_stats())
print("CPU频率:",psutil.cpu_freq()[2])
print("CPU核心统计:",psutil.cpu_count(),psutil.cpu_count(logical=False))

print("\n"+"内存部分".center(50,'-'))
print(psutil.virtual_memory())
print("空闲内存比:",psutil.virtual_memory().percent)
print("空闲物理内存:",psutil.virtual_memory().free)
print("交换分区:",psutil.swap_memory())
print(psutil.swap_memory().total)

print("\n"+"磁盘部分".center(50,'-'))
print("Disk Label\t","mount\t","FStype\t","Mode")
for x in psutil.disk_partitions():
    print(x[:])
    print(psutil.disk_usage(x[1]))


print("\n"+"网络部分".center(50,'-'))
print("网络连接信息".center(30,'*'))
for x in psutil.net_connections():
    print(x[3:5])
#print(psutil.net_if_addrs())
print("bytes_sent:",psutil.net_io_counters()[0])
print("bytes_recv:",psutil.net_io_counters()[2])

print("\n"+"其他信息部分".center(50,'-'))
print(psutil.users())
print("开机时间:",datetime.datetime.fromtimestamp(psutil.boot_time()))
durable = time.time()-psutil.boot_time()
print("在线时间:",datetime.timedelta(seconds=durable))


print("进程管理部分".center(50,'-'))
flag = 0
for x in psutil.pids():
    sel = psutil.Process(x)
    flag = 1 if sel.name().lower()=="xshell.exe" else 0
    if flag:
        print("进程路径:",sel.exe(),"\n",sel.cwd(),sel.status())
        print("进程内存使用率:",round(sel.memory_percent(),2))#,sel.memory_info(),
        print("进程CPU使用率:",round(sel.cpu_percent()))
        print("进程线程数:",sel.num_threads())
        break