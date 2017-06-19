from Serverinfo.unixtool import diskinfo,meminfo#,cpuinfo
def main():
    infodict = {}
    infodict['Mem']=meminfo.memory()
    infodict['Disk']=diskinfo.filter()

    #infodict['Cpu']=cpuinfo.get_cpu_usage()
    return infodict