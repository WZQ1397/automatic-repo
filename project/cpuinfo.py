def _read_cpu_usage(self):  
    """从/proc/stat读取当前系统cpu使用率""" 
    try:  
        fd = open("/proc/stat", 'r')  
        lines = fd.readlines()  
 
    finally:  
        if fd:  
            fd.close()  
 
    for line in lines:  
        l = line.split()  
        if len(l) < 5:  
            continue 
        if l[0].startswith('cpu'):  
            return l  
 
    return []  
   
def get_cpu_usage(self):  
    """ 
    get cpu avg used by percent 
    """ 
    cpustr=self._read_cpu_usage()  
 
    if not cpustr:  
        return 0 
 
    #cpu usage=[(user_2 +sys_2+nice_2) - (user_1 + sys_1+nice_1)]/(total_2 - total_1)*100 
 
    usni1=long(cpustr[1])+long(cpustr[2])+long(cpustr[3])+long(cpustr[5])
          +long(cpustr[6])+long(cpustr[7])+long(cpustr[4])  
    usn1=long(cpustr[1])+long(cpustr[2])+long(cpustr[3])  
 
   #usni1=long(cpustr[1])+long(cpustr[2])+long(cpustr[3])+long(cpustr[4])  
 
   # self.sleep=2  
 
    time.sleep(self.sleep)  
    cpustr=self._read_cpu_usage()  
 
    if not cpustr:  
        return 0 
 
    usni2=long(cpustr[1])+long(cpustr[2])+float(cpustr[3])+long(cpustr[5])
          +long(cpustr[6])+long(cpustr[7])+long(cpustr[4])  
    usn2=long(cpustr[1])+long(cpustr[2])+long(cpustr[3])  
    cpuper=(usn2-usn1)/(usni2-usni1)  
 
    return 100*cpupe  
