#coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2016 宝塔软件(http:#bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <2879625666@qq.com>
# +-------------------------------------------------------------------
import public,db,os,web,time,re
class crontab:
    #取计划任务列表
    def GetCrontab(self,get):
        self.checkBackup()
        cront = public.M('crontab').order("id desc").field('id,name,type,where1,where_hour,where_minute,echo,addtime').select()
        data=[]
        for i in range(len(cront)):
            tmp=cront[i]
            if cront[i]['type']=="day":
                tmp['type']=public.getMsg('CRONTAB_TODAY')
                tmp['cycle']= public.getMsg('CRONTAB_TODAY_CYCLE',(str(cront[i]['where_hour']),str(cront[i]['where_minute'])))
            elif cront[i]['type']=="day-n":
                tmp['type']=public.getMsg('CRONTAB_N_TODAY',(str(cront[i]['where1']),))
                tmp['cycle']=public.getMsg('CRONTAB_N_TODAY_CYCLE',(str(cront[i]['where1']),str(cront[i]['where_hour']),str(cront[i]['where_minute'])))
            elif cront[i]['type']=="hour":
                tmp['type']=public.getMsg('CRONTAB_HOUR')
                tmp['cycle']=public.getMsg('CRONTAB_HOUR_CYCLE',(str(cront[i]['where_minute']),))
            elif cront[i]['type']=="hour-n":
                tmp['type']=public.getMsg('CRONTAB_N_HOUR',(str(cront[i]['where1']),))
                tmp['cycle']=public.getMsg('CRONTAB_N_HOUR_CYCLE',(str(cront[i]['where1']),str(cront[i]['where_minute'])))
            elif cront[i]['type']=="minute-n":
                tmp['type']=public.getMsg('CRONTAB_N_MINUTE',(str(cront[i]['where1']),))
                tmp['cycle']=public.getMsg('CRONTAB_N_MINUTE_CYCLE',(str(cront[i]['where1']),))
            elif cront[i]['type']=="week":
                tmp['type']=public.getMsg('CRONTAB_WEEK')
                tmp['cycle']= public.getMsg('CRONTAB_WEEK_CYCLE',(self.toWeek(int(cront[i]['where1'])),str(cront[i]['where_hour']),str(cront[i]['where_minute'])))
            elif cront[i]['type']=="month":
                tmp['type']=public.getMsg('CRONTAB_MONTH')
                tmp['cycle']=public.getMsg('CRONTAB_MONTH_CYCLE',(str(cront[i]['where1']),str(cront[i]['where_hour']),str(cront[i]['where_minute'])))
            data.append(tmp)
        return data
    
    #转换大写星期
    def toWeek(self,num):
        wheres={
                0   :   public.getMsg('CRONTAB_SUNDAY'),
                1   :   public.getMsg('CRONTAB_MONDAY'),
                2   :   public.getMsg('CRONTAB_TUESDAY'),
                3   :   public.getMsg('CRONTAB_WEDNESDAY'),
                4   :   public.getMsg('CRONTAB_THURSDAY'),
                5   :   public.getMsg('CRONTAB_FRIDAY'),
                6   :   public.getMsg('CRONTAB_SATURDAY')
                }
        try:
            return wheres[num]
        except:
            return ''
    
    #检查环境
    def checkBackup(self):
        #检查备份脚本是否存在
        filePath=web.ctx.session.setupPath+'/panel/script/backup'
        if not os.path.exists(filePath):
            public.downloadFile(web.ctx.session.home + '/linux/backup.sh',filePath)
        #检查日志切割脚本是否存在
        filePath=web.ctx.session.setupPath+'/panel/script/logsBackup'
        if not os.path.exists(filePath):
            public.downloadFile(web.ctx.session.home + '/linux/logsBackup.py',filePath)
        #检查计划任务服务状态
        
        if os.path.exists('/etc/init.d/crond'): 
            if public.ExecShell('/etc/init.d/crond status')[0].find('running') == -1: public.ExecShell('/etc/init.d/crond start')
        elif os.path.exists('/etc/init.d/cron'):
            if public.ExecShell('/etc/init.d/cron status')[0].find('running') == -1: public.ExecShell('/etc/init.d/cron start')
        elif os.path.exists('/usr/lib/systemd/system/crond.service'):
            if public.ExecShell('systemctl status crond')[0].find('running') == -1: public.ExecShell('systemctl start crond')
            
    
    #添加计划任务
    def AddCrontab(self,get):
        if len(get['name'])<1:
             return public.returnMsg(False,'CRONTAB_TASKNAME_EMPTY')
        cuonConfig=""
        if get['type']=="day":
            cuonConfig = self.GetDay(get)
            name = public.getMsg('CRONTAB_TODAY')
        elif get['type']=="day-n":
            cuonConfig = self.GetDay_N(get)
            name = public.getMsg('CRONTAB_N_TODAY',(get['where1'],))
        elif get['type']=="hour":
            cuonConfig = self.GetHour(get)
            name = public.getMsg('CRONTAB_HOUR')
        elif get['type']=="hour-n":
            cuonConfig = self.GetHour_N(get)
            name = public.getMsg('CRONTAB_HOUR')
        elif get['type']=="minute-n":
            cuonConfig = self.Minute_N(get)
        elif get['type']=="week":
            get['where1']=get['week']
            cuonConfig = self.Week(get)
        elif get['type']=="month":
            cuonConfig = self.Month(get)
        cronPath=web.ctx.session.setupPath+'/cron'
        cronName=self.GetShell(get)
        if type(cronName) == dict: return cronName;
        cuonConfig += ' ' + cronPath+'/'+cronName+' >> '+ cronPath+'/'+cronName+'.log 2>&1'
        self.WriteShell(cuonConfig)
        self.CrondReload()
        addData=public.M('crontab').add('name,type,where1,where_hour,where_minute,echo,addtime',(get['name'],get['type'],get['where1'],get['hour'],get['minute'],cronName,time.strftime('%Y-%m-%d %X',time.localtime())))
        if addData>0:
             return public.returnMsg(True,'ADD_SUCCESS')
        return public.returnMsg(False,'ADD_ERROR')
        
    #取任务构造Day
    def GetDay(self,param):
        cuonConfig ="{0} {1} * * * ".format(param['minute'],param['hour'])
        return cuonConfig
    #取任务构造Day_n
    def GetDay_N(self,param):
        cuonConfig ="{0} {1} */{2} * * ".format(param['minute'],param['hour'],param['where1'])
        return cuonConfig
    
    #取任务构造Hour
    def GetHour(self,param):
        cuonConfig ="{0} * * * * ".format(param['minute'])
        return cuonConfig
    
    #取任务构造Hour-N
    def GetHour_N(self,param):
        cuonConfig ="{0} */{1} * * * ".format(param['minute'],param['where1'])
        return cuonConfig
    
    #取任务构造Minute-N
    def Minute_N(self,param):
        cuonConfig ="*/{0} * * * * ".format(param['where1'])
        return cuonConfig
    
    #取任务构造week
    def Week(self,param):
        cuonConfig ="{0} {1} * * {2}".format(param['minute'],param['hour'],param['week'])
        return cuonConfig
    
    #取任务构造Month
    def Month(self,param):
        cuonConfig = "{0} {1} {2} * * ".format(param['minute'],param['hour'],param['where1'])
        return cuonConfig
    
    #取数据列表
    def GetDataList(self,get):
        data = {}
        data['data'] = public.M(get['type']).field('name,ps').select()
        data['orderOpt'] = [];
        import json
        tmp = public.readFile('data/libList.conf');
        libs = json.loads(tmp)
        import imp;
        for lib in libs:
            try:
                imp.find_module(lib['module']);
                tmp = {}
                tmp['name'] = lib['name'];
                tmp['value']= lib['opt']
                data['orderOpt'].append(tmp);
            except:
                continue;
        return data
    
    #取任务日志
    def GetLogs(self,get):
        id = get['id']
        echo = public.M('crontab').where("id=?",(id,)).field('echo').find()
        logFile = web.ctx.session.setupPath+'/cron/'+echo['echo']+'.log'
        if not os.path.exists(logFile):return public.returnMsg(False, 'CRONTAB_TASKLOG_EMPTY')
        log = public.readFile(logFile)
        where = "Warning: Using a password on the command line interface can be insecure.\n"
        if  log.find(where)>-1:
            log = log.replace(where, '')
            public.writeFile('/tmp/read.tmp',log)
        return public.returnMsg(True, log)
    
    #清理任务日志
    def DelLogs(self,get):
        try:
            id = get['id']
            echo = public.M('crontab').where("id=?",(id,)).getField('echo')
            logFile = web.ctx.session.setupPath+'/cron/'+echo+'.log'
            os.remove(logFile)
            return public.returnMsg(True, 'CRONTAB_TASKLOG_CLOSE')
        except:
            return public.returnMsg(False, 'CRONTAB_TASKLOG_CLOSE_ERR')
    
    #删除计划任务
    def DelCrontab(self,get):
        try:
            id = get['id']
            find = public.M('crontab').where("id=?",(id,)).field('name,echo').find()
            x = web.ctx.session.server_os['x'];
            if x == 'RHEL':
                file='/var/spool/cron/root'
            else:
                file='/var/spool/cron/crontabs/root'
            conf=public.readFile(file)
            rep = ".+" + str(find['echo']) + ".+\n"
            conf = re.sub(rep, "", conf)
            cronPath = web.ctx.session.setupPath + '/cron'
            public.writeFile(file,conf)
            
            sfile = cronPath + '/' + find['echo']
            if os.path.exists(sfile): os.remove(sfile)
            sfile = cronPath + '/' + find['echo'] + '.log'
            if os.path.exists(sfile): os.remove(sfile)
            
            self.CrondReload()
            public.M('crontab').where("id=?",(id,)).delete()
            public.WriteLog('TYPE_CRON', 'CRONTAB_DEL',(find['name'],))
            return public.returnMsg(True, 'DEL_SUCCESS')
        except:
            return public.returnMsg(False, 'DEL_ERROR')
    
    #取执行脚本
    def GetShell(self,param):
        try:
            type=param['sType']
            if type=='toFile':
                shell=param.sFile
            else :
                head="#!/bin/bash\nPATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin\nexport PATH\n"
                log='-access_log'
                if web.ctx.session.webserver=='nginx':
                    log='.log'
                
                wheres={
                        'site'  :   head + "python " + web.ctx.session.setupPath+"/panel/script/backup.py site "+param['sName']+" "+param['save'],
                        'database': head + "python " + web.ctx.session.setupPath+"/panel/script/backup.py database "+param['sName']+" "+param['save'],
                        'logs'  :   head + "python " + web.ctx.session.setupPath+"/panel/script/logsBackup "+param['sName']+log+" "+param['save'],
                        'rememory' : head + "/bin/bash " + web.ctx.session.setupPath + '/panel/script/rememory.sh'
                        }
                if param['backupTo'] != 'localhost':
                    cfile = web.ctx.session.setupPath + "/panel/plugin/" + param['backupTo'] + "/" + param['backupTo'] + "_main.py";
                    if not os.path.exists(cfile): cfile = web.ctx.session.setupPath + "/panel/script/backup_" + param['backupTo'] + ".py";
                    
                    wheres={
                        'site'  :   head + "python " + cfile + " site " + param['sName'] + " " + param['save'],
                        'database': head + "python " + cfile + " database " + param['sName'] + " " + param['save'],
                        'logs'  :   head + "python " + web.ctx.session.setupPath+"/panel/script/logsBackup "+param['sName']+log+" "+param['save'],
                        'rememory' : head + "/bin/bash " + web.ctx.session.setupPath + '/panel/script/rememory.sh'
                        }              
                
                try:
                    shell=wheres[type]
                except:
                    if type == 'toUrl':
                        shell = head + "curl -sS --connect-timeout 10 -m 60 '" + param.urladdress+"'"; 
                    else:
                        shell=head+param['sBody']
                    
                    shell += '''
echo "----------------------------------------------------------------------------"
endDate=`date +"%Y-%m-%d %H:%M:%S"`
echo "★[$endDate] Successful"
echo "----------------------------------------------------------------------------"
'''
            cronPath=web.ctx.session.setupPath+'/cron'
            if not os.path.exists(cronPath): public.ExecShell('mkdir -p ' + cronPath);
            cronName=public.md5(public.md5(str(time.time()) + '_bt'))
            file = cronPath+'/' + cronName
            public.writeFile(file,self.CheckScript(shell))
            public.ExecShell('chmod 750 ' + file)
            return cronName
        except Exception,ex:
            return public.returnMsg(False, 'FILE_WRITE_ERR')
        
    #检查脚本
    def CheckScript(self,shell):
        keys = ['shutdown','init 0','mkfs','passwd','chpasswd','--stdin','mkfs.ext','mke2fs']
        for key in keys:
            shell = shell.replace(key,'[***]');
        return shell;
    
    #重载配置
    def CrondReload(self):
        if os.path.exists('/etc/init.d/crond'): 
            public.ExecShell('/etc/init.d/crond reload')
        elif os.path.exists('/etc/init.d/cron'):
            public.ExecShell('service cron restart')
        else:
            public.ExecShell("systemctl reload crond")
        
    #将Shell脚本写到文件
    def WriteShell(self,config):
        x = web.ctx.session.server_os['x'];
        if x == 'RHEL':
            file='/var/spool/cron/root'
        else:
            file='/var/spool/cron/crontabs/root'
        
        if not os.path.exists(file): public.writeFile(file,'')
        conf = public.readFile(file)
        conf += config + "\n"
        if public.writeFile(file,conf):
            if x == 'RHEL':
                public.ExecShell("chmod 600 '" + file + "' && chown root.root " + file)
            else:
                public.ExecShell("chmod 600 '" + file + "' && chown root.crontab " + file)
            return True
        return public.returnMsg(False,'FILE_WRITE_ERR')
    
    #立即执行任务
    def StartTask(self,get):
        echo = public.M('crontab').where('id=?',(get.id,)).getField('echo');
        execstr = web.ctx.session.setupPath + '/cron/' + echo;
        os.system('chmod +x ' + execstr)
        os.system('nohup ' + execstr + ' >> ' + execstr + '.log 2>&1 &');
        return public.returnMsg(True,'CRONTAB_TASK_EXEC')
        
    
        