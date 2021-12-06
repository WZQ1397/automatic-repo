# coding=UTF-8
import time, os, sys, json
import datetime


class Config:
    timeformat = '%Y%m%d'
    #sday = '20200217'
    #eday = '20200219'
    today = datetime.datetime.today()
    befor_61=today-datetime.timedelta(days=61)
    befor_60=today-datetime.timedelta(days=60)
    sday=befor_61.strftime('%Y%m%d')
    eday=befor_60.strftime('%Y%m%d')


    applist = ['']

    tmp_path = "/home/data1/zach/tmp_path"  # 下载hdfs和ftp的临时保存路径
    zip_path = "/home/data2/zach/app/c5data/upload"  # 压缩备份程序保存路径
    ftp_path = "/home/ftpdir/ziplog/app/c5data"  # 10.110.142.4 上
    hdfs_path = "hdfs:////user/zach/ziplog/app/c5data/upload"  # 压缩文件在hdfs上的保存路径

    # 保存比对结果
    rootpath = sys.path[0]
    result_path = os.path.join(rootpath, "result_zip")
    if not os.path.exists(result_path): os.makedirs(result_path)

def strtime2linuxtime(strtime, timeformat):
    linuxtime = time.mktime(time.strptime(strtime, timeformat))
    return int(linuxtime)

# 将linux时间(int或者float型)转换为'timeformat'格式的字符串时间
def linuxtime2strtime(linuxtime, timeformat):
    strtime = time.strftime(timeformat, time.localtime(float(linuxtime)))
    return strtime

def reset_path(tmp_path):
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    else:
        os.system("rm -rf {tmp_path}".format(tmp_path=tmp_path))
        os.makedirs(tmp_path)
        pass

def cmp_file(file1, file2):
    '''
    :param file1:
    :param file2:
    :return:
    '''

    result = list()
    cmd="cmp --silent {f1} {f2}".format(f1=file1, f2=file2)
    print cmd
    shell_str = "cmp --silent {f1} {f2}  && echo 'same' || echo 'diff'".format(f1=file1, f2=file2)
    shell_res = os.popen(shell_str).readlines()[0].replace('\n', '')

    if shell_res == "same":
        pass
    elif shell_res == "diff":
        result = "diff"
    else:
        result = "other"

    return result


def main_cmp(stime, etime, TIMEFORMAT, local_path, hdfs_path, ftp_path, tmp_path, result_path):
    hdfs_save_path = os.path.join(tmp_path, "hdfs")
    ftp_save_path = os.path.join(tmp_path, "ftp")

    for daytime in range(stime, etime, 24 * 3600):

        reset_path(hdfs_save_path)
        reset_path(ftp_save_path)

        daydate = linuxtime2strtime(daytime, TIMEFORMAT)
        year, month, day = daydate[0:4], daydate[4:6], daydate[6:8]
        new_daydate=year+"-"+month+"-"+day
        time0 = int(time.time())

        #print "\nstart_time:", linuxtime2strtime(time0, "%Y/%m/%d %H:%M:%S"), "deal day", daydate

        # 比较本地和hdfs
        result = {"not_exit": []}
        filename="c5data-{ymd}.zip".format(ymd=new_daydate)

        # 获取 hdfs 到本地
        os.system("hadoop fs -get {hdfs_path}/{filename} {save_path}".format(hdfs_path=os.path.join(hdfs_path),  save_path=hdfs_save_path, filename=filename))


        # 获取 ftp 到本地
        os.system(" sshpass -p 'QWERasdfZXCV1234' rsync -t -rv zach@10.110.142.4:{ftp_path}/{filename} {save_path}"\
            .format(ftp_path=os.path.join(ftp_path, "upload"), save_path=ftp_save_path, filename=filename))
        
        tmp_hdfs_f = os.path.join(hdfs_save_path, filename)
        tmp_ftp_f = os.path.join(ftp_save_path, filename)
        local_f = os.path.join(local_path, filename)

        ## 查看是否存在
        flag_local, flag_ftp, flag_hdfs = True, True, True
        if not os.path.exists(local_f):
            result["not_exit"].append(local_path)
            #result["not_exit"].append(os.path.join(local_path, daydate))
            flag_local = False
        if not os.path.exists(tmp_ftp_f):
            result["not_exit"].append(ftp_path)
            #result["not_exit"].append(os.path.join(ftp_path, daydate))
            flag_ftp = False
        if not os.path.exists(tmp_hdfs_f):
            result["not_exit"].append(hdfs_path)
            #result["not_exit"].append(os.path.join(hdfs_path, daydate))
            flag_hdfs = False

        if flag_local & flag_ftp:
            result_i = cmp_file(local_f, tmp_ftp_f)
            if len(result_i) > 0:
                result["local_ftp"] = [result_i, [local_path, ftp_path]]

        if flag_local & flag_hdfs:
            result_i = cmp_file(local_f, tmp_hdfs_f)
            if len(result_i) > 0:
                result["local_hdfs"] = [result_i, [local_path, hdfs_path]]

        if flag_ftp & flag_hdfs:
            result_i = cmp_file(tmp_ftp_f, tmp_hdfs_f)
            if len(result_i) > 0:
                result["ftp_hdfs"] = [result_i, [ftp_path, hdfs_path]]

        ### 保存result 写入时间和结果
        # 日志记载
        cost_time = int(time.time()) - time0
        s = "{now_t} --- deal {day}, cost_time:{cost_time}s, path:{path}\n".format(now_t=linuxtime2strtime( time.time(), '%Y/%m/%d %H:%M:%S' ),
                                                                                   day=daydate, cost_time=str(cost_time),
                                                                                   path=local_path)  # 当前时间，日期，耗时, 处理的文件夹 / 处理结果/换行
        print result
        print result_path
        print "log:", s



        with open(os.path.join(result_path, "log.txt"), 'a+') as f:
            f.write(s)

        # 结果记录
        with open(os.path.join(result_path, "result_{day}.json".format(day=daydate)), 'w') as json_file:
            json.dump(result, json_file)


if __name__ == '__main__':

    applist = Config.applist
    timeformat = Config.timeformat

    # 输入比对时间范围
    try:
        sday = sys.argv[1]
        eday = sys.argv[2]
    except:
        sday = Config.sday
        eday = Config.eday

    stime, etime = strtime2linuxtime(sday, timeformat), strtime2linuxtime(eday, timeformat)
    print "程序开始，比较数据的日期范围为", sday, eday

    if len(applist) > 0:  # 对于不同app这种，再加一层路径进行比较
        for app in applist:
            print "\n********************** deal app:", app
            tmp_path = os.path.join(Config.tmp_path, app)
            zip_path = os.path.join(Config.zip_path, app)
            ftp_path = os.path.join(Config.ftp_path, app)
            hdfs_path = os.path.join(Config.hdfs_path, app)

            result_path = os.path.join(Config.result_path, app)
            if not os.path.exists(result_path): os.makedirs(result_path)

            main_cmp(stime, etime, timeformat, zip_path, hdfs_path, ftp_path, tmp_path, result_path)

    else:

        if not os.path.exists(Config.result_path): os.makedirs(Config.result_path)
        main_cmp(stime, etime, timeformat, Config.zip_path, Config.hdfs_path, Config.ftp_path, Config.tmp_path,
                 Config.result_path)
        pass

    # print(__name__)
