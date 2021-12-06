# coding=UTF-8
import time
import datetime
import os
import sys
import json

def strtime2linuxtime(strtime, timeformat):
    linuxtime = time.mktime(time.strptime(strtime, timeformat))
    return int(linuxtime)
# 将linux时间(int或者float型)转换为'timeformat'格式的字符串时间
def linuxtime2strtime(linuxtime, timeformat):
    strtime = time.strftime(timeformat, time.localtime(float(linuxtime)))
    return strtime

rootpath=sys.path[0]


tmp_path= "/home/data1/zach/tmp_path"
#tmp_path= os.path.join(rootpath, "tmp_path")

os.system("rm -rf {tmp_path}".format(tmp_path=tmp_path))
if not os.path.exists(tmp_path): os.makedirs(tmp_path)
print "tmp_path", tmp_path

zip_path= "/home/data2/zach/app/c5data/upload"
ref_path= "/home/data2/zach/app/c5data"

#zip_path =  "/Users/jiangsanmu/Desktop/code/compare_data/arrangement_data/ziplog"
#ref_path =  "/Users/jiangsanmu/Desktop/code/compare_data/arrangement_data/ori"

#applist = ['cctv5', 'cctvchild', 'cctvfinance', 'cctvmusic', 'cctvopera', 'newsm']
applist = ['']

# 保存比对结果
result_path=os.path.join(rootpath, "result")
if not os.path.exists(result_path): os.makedirs(result_path)

# 输入比对时间范围
try:
    sday = sys.argv[1]
    eday = sys.argv[2]
except:
    sday='20200217'
    eday='20200218'

    today = datetime.datetime.today()
    befor_61=today-datetime.timedelta(days=61)
    befor_60=today-datetime.timedelta(days=60)
    sday=befor_61.strftime('%Y%m%d')
    eday=befor_60.strftime('%Y%m%d')

print "比对日期范围", sday, eday

timeformat='%Y%m%d'
stime = strtime2linuxtime(sday, timeformat)
etime = strtime2linuxtime(eday, timeformat)



def compare(ob_path, zip_path):
    '''
    :param ob_path: 如 ori/cctv5/2020217/2200，比对作为查看的文件夹，路径范围到 小时分钟
    :param zip_path: 如 ziplog/cctv5/20200217/2200， 解压之后的文件夹，和 ob_path 一一对应，路径范围到 小时分钟
    :return:
    '''

    result = {"path_not_exist": {}, "set_o2z": [], "set_z2o": [], "diff": [], "other": []}

    flag = True #检测路径是否存在
    if not os.path.exists(ob_path):
        result["path_not_exist"]["object"] = ob_path
        flag = False

    if not os.path.exists(zip_path):
        result["path_not_exist"]["zip"] = zip_path
        flag = False
    # 直接返回
    if not flag:
        return flag, result

    flag=True # 检测路径不是文件夹的情况
    try:
        ob_files = set(os.listdir(os.path.join(ob_path)))
        print ob_files 
    except:
        flag = False
        result["ob_notPath"] = ob_path
    print zip_path
    try:
        zip_files = set(os.listdir(os.path.join(zip_path)))
        print zip_files
    except:
        flag = False
        result["zip_notPath"] = zip_path
    # 直接返回
    if not flag:
        return flag, result
    '''
    # 比对文件夹下的差异
    set_o2z, set_z2o = ob_files - zip_files, zip_files - ob_files

    result["len_ob"] = len(ob_files)
    result["len_zip"] = len(zip_files)

    if len(set_o2z) != 0:
        result["set_o2z"] = sorted(list(set_o2z), reverse=False)
        flag = False

    if len(set_z2o) != 0:
        result["set_z2o"] = sorted(list(set_z2o), reverse=False)
        flag = False
    '''
    # 比对相同的文件
    for fl in ob_files & zip_files:

        cmd="cmp --silent {f1} {f2}".format(f1=os.path.join(ob_path, fl),f2=os.path.join(zip_path, fl))
        print cmd
        shell_str = "cmp --silent {f1} {f2}  && echo 'same' || echo 'diff'".format(f1=os.path.join(ob_path, fl),
                                                                                   f2=os.path.join(zip_path, fl))

        shell_res = os.popen(shell_str).readlines()[0].replace('\n', '')
        if shell_res == "same":
            continue
        elif shell_res == "diff":
            result["diff"].append(fl)
            #if fl=="NAV.json": print os.path.join(ob_path, fl), os.path.join(tmp_path, fl)
            flag = False
        else:
            result["other"].append(fl)
            flag = False

    return flag, result



def compare_day(ob_path, zip_file, tmp_path, daydate):
    '''
    :param ob_path:  如 ori/cctv5/2020217/，下有文件夹 2200 2205 2210 2215 2220 2225 2230等，比对作为查看的文件夹，路径范围到天
    :param zip_file: 如 ziplog/cctv5/20200217，下有20200217.zip压缩文件，路径范围到天
    :param tmp_path:  临时保存路径，不重要
    :return:
    '''
    print "======== start ======="
    print "Ori path:"+ob_path
    print "Compress path:"+zip_file

    result = {"path_not_exist":{}, "path_set_o2z":[], "path_set_z2o":[], "HourMinPath":[]}
    flag = True

    if not os.path.exists(ob_path):
        result["path_not_exist"]["object"] = ob_path
        flag = False

    if not os.path.exists( zip_file):
        result["path_not_exist"]["zip"] = zip_file
        flag = False

    if not flag:
        return result

    os.popen("unzip {zip_file} -d {tmp_path}".format(zip_file=zip_file, tmp_path=tmp_path))
    #os.popen("tar zxf {zip_file} -C {tmp_path}".format(zip_file=zip_file, tmp_path=tmp_path))
    
    ''' 
    # 天文件夹下比较 "小时分钟"文件夹 的差异
    ob_paths = set(os.listdir(ob_path))
    zip_paths = set(os.listdir(tmp_path))
    path_set_o2z, path_set_z2o = ob_paths - zip_paths, zip_paths - ob_paths
    
    if len(path_set_o2z) !=0:
        result["path_set_o2z"]= sorted(list(path_set_o2z), reverse=False)
    if len(path_set_z2o) !=0:
        result["path_set_z2o"]= sorted(list(path_set_z2o), reverse=False)

    result["len_path_ob"] = len(ob_paths)
    result["len_path_zip"] = len(zip_paths)
    '''

    # 比较共同的"小时分钟"文件夹
    #for p in  ob_paths & zip_paths:
    p_flag, p_result= compare( ob_path, tmp_path+"/"+daydate) 
    print "------------------  p_flag, p_result", p_flag, p_result
    if not p_flag: # 出现了异常情况
        result["HourMinPath"].append({ob_path:p_result})
    print ob_path +" ==> "+str(result)
    return result


for daytime in range(stime, etime, 24*3600):
    daydate=linuxtime2strtime(daytime, timeformat )
    year, month, day = daydate[0:4], daydate[4:6], daydate[6:8]
    time0 = int(time.time())
    new_daydate=year+"/"+month+"/"+day
   
    print "\nstart_time:", linuxtime2strtime(time0, "%Y/%m/%d %H:%M:%S"), "deal day",new_daydate
    
    for app in applist:
        print app

        #zip_file= os.path.join(zip_path, app, daydate, "{ymd}.zip".format(ymd=daydate))
        zip_file= os.path.join(zip_path, "c5data-{ymd}.zip".format(ymd=new_daydate.replace("/","-")))
        #zip_file= os.path.join(zip_path, "c5data-{ymd}.tar.gz".format(ymd=new_daydate.replace("/","-")))
        #zip_file= os.path.join(zip_path, app, new_daydate, "{ymd}.tar.gz".format(ymd=daydate))
        print zip_file
        os.system("rm -rf {tmp_path}".format(tmp_path=tmp_path))
        if not os.path.exists(tmp_path): os.makedirs(tmp_path)
        result = compare_day( os.path.join(ref_path, app, new_daydate), zip_file, tmp_path, new_daydate)

        result_path_app = os.path.join(result_path, app)
        if not os.path.exists(result_path_app): os.makedirs(result_path_app)
        with open(os.path.join(result_path_app, "result_{day}.json".format(day=daydate)), 'w') as json_file:
            json.dump(result, json_file)

    #print "result", result
    print "cost_time", int(time.time()) - time0




