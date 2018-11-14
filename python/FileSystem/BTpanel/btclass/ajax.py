 #coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2016 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <2879625666@qq.com>
# +-------------------------------------------------------------------
import public,os,web
class ajax:
    
    def GetNginxStatus(self,get):
        #取Nginx负载状态
        self.CheckStatusConf();
        result = public.httpGet('http://127.0.0.1/nginx_status')
        tmp = result.split()
        data = {}
        data['active']   = tmp[2]
        data['accepts']  = tmp[9]
        data['handled']  = tmp[7]
        data['requests'] = tmp[8]
        data['Reading']  = tmp[11]
        data['Writing']  = tmp[13]
        data['Waiting']  = tmp[15]
        return data
    
    def GetPHPStatus(self,get):
        #取指定PHP版本的负载状态
        self.CheckStatusConf();
        import json,time,web
        version = web.input(version='54').version
        result = public.httpGet('http://127.0.0.1/phpfpm_'+version+'_status?json')
        tmp = json.loads(result)
        fTime = time.localtime(int(tmp['start time']))
        tmp['start time'] = time.strftime('%Y-%m-%d %H:%M:%S',fTime)
        return tmp
    
    def CheckStatusConf(self):
        if web.ctx.session.webserver != 'nginx': return;
        filename = web.ctx.session.setupPath + '/panel/vhost/nginx/phpfpm_status.conf';
        if os.path.exists(filename): return;
        
        conf = '''server {
    listen 80;
    server_name 127.0.0.1;
    allow 127.0.0.1;
    location /nginx_status {
        stub_status on;
        access_log off;
    }
    location /phpfpm_52_status {
        fastcgi_pass unix:/tmp/php-cgi-52.sock;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME \$fastcgi_script_name;
    }
    location /phpfpm_53_status {
        fastcgi_pass unix:/tmp/php-cgi-53.sock;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME \$fastcgi_script_name;
    }
    location /phpfpm_54_status {
        fastcgi_pass unix:/tmp/php-cgi-54.sock;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME \$fastcgi_script_name;
    }
    location /phpfpm_55_status {
        fastcgi_pass unix:/tmp/php-cgi-55.sock;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME \$fastcgi_script_name;
    }
    location /phpfpm_56_status {
        fastcgi_pass unix:/tmp/php-cgi-56.sock;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME \$fastcgi_script_name;
    }
    location /phpfpm_70_status {
        fastcgi_pass unix:/tmp/php-cgi-70.sock;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME \$fastcgi_script_name;
    }
    location /phpfpm_71_status {
        fastcgi_pass unix:/tmp/php-cgi-71.sock;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME \$fastcgi_script_name;
    }
}'''
        public.writeFile(filename,conf);
        public.serviceReload();
    
    
    def GetTaskCount(self,get):
        #取任务数量
        return public.M('tasks').where("status!=?",('1',)).count()
    
    def GetSoftList(self,get):
        #取软件列表
        import json,os,web
        tmp = public.readFile('data/softList.conf');
        data = json.loads(tmp)
        tasks = public.M('tasks').where("status!=?",('1',)).field('status,name').select()
        for i in range(len(data)):
            data[i]['check'] = web.ctx.session.rootPath+'/'+data[i]['check'];
            for n in range(len(data[i]['versions'])):
                #处理任务标记
                isTask = '1';
                for task in tasks:
                    tmp = public.getStrBetween('[',']',task['name'])
                    if not tmp:continue;
                    tmp1 = tmp.split('-');
                    if data[i]['name'] == 'PHP': 
                        if tmp1[0].lower() == data[i]['name'].lower() and tmp1[1] == data[i]['versions'][n]['version']: isTask = task['status'];
                    else:
                        if tmp1[0].lower() == data[i]['name'].lower(): isTask = task['status'];
                
                #检查安装状态
                if data[i]['name'] == 'PHP': 
                    data[i]['versions'][n]['task'] = isTask
                    checkFile = data[i]['check'].replace('VERSION',data[i]['versions'][n]['version'].replace('.',''));
                else:
                    data[i]['task'] = isTask
                    version = public.readFile(web.ctx.session.rootPath+'/server/'+data[i]['name'].lower()+'/version.pl');
                    if not version:continue;
                    if version.find(data[i]['versions'][n]['version']) == -1:continue;
                    checkFile = data[i]['check'];
                data[i]['versions'][n]['status'] = os.path.exists(checkFile);
        return data
    
    
    def GetLibList(self,get):
        #取插件列表
        import json,os,web
        tmp = public.readFile('data/libList.conf');
        data = json.loads(tmp)
        for i in range(len(data)):
            data[i]['status'] = self.CheckLibInstall(data[i]['check']);
            data[i]['optstr'] = self.GetLibOpt(data[i]['status'], data[i]['opt']);
        return data
    
    def CheckLibInstall(self,checks):
        for cFile in checks:
            if os.path.exists(cFile): return '已安装';
        return '未安装';
    
    #取插件操作选项
    def GetLibOpt(self,status,libName):
        optStr = '';
        if status == '未安装':
            optStr = '<a class="link" href="javascript:InstallLib(\''+libName+'\');">安装</a>';
        else:
            libConfig = '配置';
            if(libName == 'beta'): libConfig = '内测资料';
                                  
            optStr = '<a class="link" href="javascript:SetLibConfig(\''+libName+'\');">'+libConfig+'</a> | <a class="link" href="javascript:UninstallLib(\''+libName+'\');">卸载</a>';
        return optStr;
    
    #取插件AS
    def GetQiniuAS(self,get):
        filename = web.ctx.session.setupPath + '/panel/data/'+get.name+'As.conf';
        if not os.path.exists(filename): public.writeFile(filename,'');
        data = {}
        data['AS'] = public.readFile(filename).split('|');
        data['info'] = self.GetLibInfo(get.name);
        if len(data['AS']) < 3:
            data['AS'] = ['','','',''];
        return data;


    #设置插件AS
    def SetQiniuAS(self,get):
        info = self.GetLibInfo(get.name);
        filename = web.ctx.session.setupPath + '/panel/data/'+get.name+'As.conf';
        conf = get.access_key.strip() + '|' + get.secret_key.strip() + '|' + get.bucket_name.strip() + '|' + get.bucket_domain.strip();
        public.writeFile(filename,conf);
        public.ExecShell("chmod 600 " + filename)
        result = public.ExecShell("python " + web.ctx.session.setupPath + "/panel/script/backup_"+get.name+".py list")
        
        if result[0].find("ERROR:") == -1: 
            public.WriteLog("插件管理", "设置插件["+info['name']+"]AS!");
            return public.returnMsg(True, '设置成功!');
        return public.returnMsg(False, 'ERROR: 无法连接到'+info['name']+'服务器,请检查[AK/SK/存储空间]设置是否正确!');
    
    #设置内测
    def SetBeta(self,get):
        data = {}
        data['username'] = get.bbs_name
        data['qq'] = get.qq
        data['email'] = get.email
        result = public.httpPost(web.ctx.session.home + '/Api/LinuxBeta',data);
        import json;
        data = json.loads(result);
        if data['status']:
            public.writeFile('data/beta.pl',get.bbs_name + '|' + get.qq + '|' + get.email);
        return data;
    #取内测资格状态
    def GetBetaStatus(self,get):
        try:
            return public.readFile('data/beta.pl').strip();
        except:
            return 'False';
               

    #获取指定插件信息
    def GetLibInfo(self,name):
        import json
        tmp = public.readFile('data/libList.conf');
        data = json.loads(tmp)
        for lib in data:
            if name == lib['opt']: return lib;
        return False;

    #获取文件列表
    def GetQiniuFileList(self,get):
        try:
            import json             
            result = public.ExecShell("python " + web.ctx.session.setupPath + "/panel/script/backup_"+get.name+".py list")
            return json.loads(result[0]);
        except:
            return public.returnMsg(False, '获取列表失败,请检查[AK/SK/存储空间]设是否正确!');

    
    
    #取网络连接列表
    def GetNetWorkList(self,get):
        import psutil
        netstats = psutil.net_connections()
        networkList = []
        for netstat in netstats:
            tmp = {}
            if netstat.type == 1:
                tmp['type'] = 'tcp'
            else:
                tmp['type'] = 'udp'
            tmp['family']   = netstat.family
            tmp['laddr']    = netstat.laddr
            tmp['raddr']    = netstat.raddr
            tmp['status']   = netstat.status
            p = psutil.Process(netstat.pid)
            tmp['process']  = p.name()
            tmp['pid']      = netstat.pid
            networkList.append(tmp)
            del(p)
            del(tmp)
        networkList = sorted(networkList, key=lambda x : x['status'], reverse=True);
        return networkList;
    
    #取进程列表
    def GetProcessList(self,get):
        import psutil,pwd
        Pids = psutil.pids();
        
        processList = []
        for pid in Pids:
            try:
                tmp = {}
                p = psutil.Process(pid);
                if p.exe() == "": continue;
                
                tmp['name'] = p.name();                             #进程名称
                if self.GoToProcess(tmp['name']): continue;
                
                
                tmp['pid'] = pid;                                   #进程标识
                tmp['status'] = p.status();                         #进程状态
                tmp['user'] = p.username();                         #执行用户
                cputimes = p.cpu_times()    
                if cputimes.user > 100:
                    tmp['cpu_percent'] = p.cpu_percent(interval = 0.5);
                else:
                    tmp['cpu_percent'] = 0.0
                tmp['cpu_times'] = cputimes.user                             #进程占用的CPU时间
                tmp['memory_percent'] = round(p.memory_percent(),3)          #进程占用的内存比例
                pio = p.io_counters()
                tmp['io_write_bytes'] = pio.write_bytes             #进程总共写入字节数
                tmp['io_read_bytes'] = pio.read_bytes               #进程总共读取字节数
                tmp['threads'] = p.num_threads()                    #进程总线程数
                
                processList.append(tmp);
                del(p)
                del(tmp)
            except:
                continue;
        import operator
        processList = sorted(processList, key=lambda x : x['memory_percent'], reverse=True);
        processList = sorted(processList, key=lambda x : x['cpu_times'], reverse=True);
        return processList
    
    #结束指定进程
    def KillProcess(self,get):
        #return public.returnMsg(False,'演示服务器，禁止此操作!');
        import psutil
        p = psutil.Process(int(get.pid));
        name = p.name();
        if name == 'python': return public.returnMsg(False,'KILL_PROCESS_ERR');
        
        p.kill();
        public.WriteLog('TYPE_PROCESS','KILL_PROCESS',(get.pid,name));
        return public.returnMsg(True,'KILL_PROCESS',(get.pid,name));
    
    def GoToProcess(self,name):
        ps = ['sftp-server','login','nm-dispatcher','irqbalance','qmgr','wpa_supplicant','lvmetad','auditd','master','dbus-daemon','tapdisk','sshd','init','ksoftirqd','kworker','kmpathd','kmpath_handlerd','python','kdmflush','bioset','crond','kthreadd','migration','rcu_sched','kjournald','iptables','systemd','network','dhclient','systemd-journald','NetworkManager','systemd-logind','systemd-udevd','polkitd','tuned','rsyslogd']
        
        for key in ps:
            if key == name: return True
        
        return False
        
    
    def GetNetWorkIo(self,get):
        #取指定时间段的网络Io
        data =  public.M('network').dbfile('system').where("addtime>=? AND addtime<=?",(get.start,get.end)).field('id,up,down,total_up,total_down,down_packets,up_packets,addtime').order('id asc').select()
        return self.ToAddtime(data);
    
    def GetDiskIo(self,get):
        #取指定时间段的磁盘Io
        data = public.M('diskio').dbfile('system').where("addtime>=? AND addtime<=?",(get.start,get.end)).field('id,read_count,write_count,read_bytes,write_bytes,read_time,write_time,addtime').order('id asc').select()
        return self.ToAddtime(data);
    def GetCpuIo(self,get):
        #取指定时间段的CpuIo
        data = public.M('cpuio').dbfile('system').where("addtime>=? AND addtime<=?",(get.start,get.end)).field('id,pro,mem,addtime').order('id asc').select()
        return self.ToAddtime(data,True);
    
    
    def ToAddtime(self,data,tomem = False):
        import time
        #格式化addtime列
        
        if tomem:
            import psutil
            mPre = (psutil.virtual_memory().total / 1024 / 1024) / 100
        length = len(data);
        he = 1;
        if length > 100: he = 2;
        if length > 1000: he = 8;
        if length > 10000: he = 20;
        if he == 1:
            for i in range(length):
                data[i]['addtime'] = time.strftime('%m/%d %H:%M',time.localtime(float(data[i]['addtime'])))
                if tomem and data[i]['mem'] > 100: data[i]['mem'] = data[i]['mem'] / mPre
            
            return data
        else:
            count = 0;
            tmp = []
            for value in data:
                if count < he: 
                    count += 1;
                    continue;
                value['addtime'] = time.strftime('%m/%d %H:%M',time.localtime(float(value['addtime'])))
                if tomem and value['mem'] > 100: value['mem'] = value['mem'] / mPre
                tmp.append(value);
                count = 0;
            return tmp;
        
    def GetInstalleds(self,softlist):
        softs = '';
        for soft in softlist['data']:
            try:
                for v in soft['versions']:
                    if v['status']: softs += soft['name'] + '-' + v['version'] + '|';
            except:
                pass
        return softs;
    
    def UpdatePanel(self,get):
        #return public.returnMsg(False,'演示服务器，禁止此操作!');
        try:
            if not public.IsRestart(): return public.returnMsg(False,'EXEC_ERR_TASK');
            import web,json
            if int(web.ctx.session.config['status']) == 0:
                public.httpGet(web.ctx.session.home+'/Api/SetupCount?type=Linux');
                public.M('config').where("id=?",('1',)).setField('status',1);
            
            #取回远程版本信息
            if hasattr(web.ctx.session,'updateInfo') == True and hasattr(get,'check') == False:
                updateInfo = web.ctx.session.updateInfo;
            else:
                login_temp = 'data/login.temp';
                if os.path.exists(login_temp):
                    logs = public.readFile(login_temp)
                    os.remove(login_temp);
                else:
                    logs = '';
                import psutil,panelPlugin,system;
                mem = psutil.virtual_memory();
                mplugin = panelPlugin.panelPlugin();
                panelsys = system.system();
                data = {}
                data['sites'] = str(public.M('sites').count());
                data['ftps'] = str(public.M('ftps').count());
                data['databases'] = str(public.M('databases').count());
                data['system'] = panelsys.GetSystemVersion() + '|' + str(mem.total / 1024 / 1024) + 'MB|' + public.getCpuType() + '*' + str(psutil.cpu_count()) + '|' + web.ctx.session.webserver + '|' + web.ctx.session.version;
                data['system'] += '||'+self.GetInstalleds(mplugin.getPluginList(None));
                data['logs'] = logs
                msg = public.getMsg('PANEL_UPDATE_MSG');
                sUrl = web.ctx.session.home + '/Api/updateLinux';
                betaIs = 'data/beta.pl';
                betaStr = public.readFile(betaIs);
                if betaStr:
                    if betaStr.strip() != 'False':
                        sUrl = web.ctx.session.home + '/Api/updateLinuxBeta';
                        msg = public.getMsg('PANEL_UPDATE_MSG_TEST');
                
                betaIs = 'plugin/beta/config.conf';
                betaStr = public.readFile(betaIs);
                if betaStr:
                    if betaStr.strip() != 'False':
                        sUrl = web.ctx.session.home + '/Api/updateLinuxBeta';
                        msg = public.getMsg('PANEL_UPDATE_MSG_TEST');
                
                updateInfo = json.loads(public.httpPost(sUrl,data));
                if not updateInfo: return public.returnMsg(False,"CONNECT_ERR");
                updateInfo['msg'] = msg;
                web.ctx.session.updateInfo = updateInfo;
                
            #检查是否需要升级
            if updateInfo['version'] == web.ctx.session.version:
                try:
                    return public.returnMsg(False,updateInfo['msg']);
                except:
                    return public.returnMsg(False,'PANEL_UPDATE_ERR_NEW');
            
            
            #是否执行升级程序 
            if(updateInfo['force'] == True or hasattr(get,'toUpdate') == True or os.path.exists('data/autoUpdate.pl') == True):
                setupPath = web.ctx.session.setupPath;
                uptype = 'update';
                betaIs = 'plugin/beta/config.conf';
                betaStr = public.readFile(betaIs);
                if betaStr:
                    if betaStr.strip() != 'False': uptype = 'updateTest';
                betaIs = 'data/beta.pl';
                betaStr = public.readFile(betaIs);
                if betaStr:
                    if betaStr.strip() != 'False': uptype = 'updateTest';
                httpUrl = public.get_url();
                if httpUrl: updateInfo['downUrl'] =  httpUrl + '/install/' + uptype + '/LinuxPanel-' + updateInfo['version'] + '.zip';
                
                public.downloadFile(updateInfo['downUrl'],'panel.zip');
                if os.path.getsize('panel.zip') < 1048576: return public.returnMsg(False,"PANEL_UPDATE_ERR_DOWN");
                public.ExecShell('unzip -o panel.zip -d ' + setupPath + '/');
                import compileall
                if os.path.exists(setupPath + '/panel/main.py'): public.ExecShell('rm -f ' + setupPath + '/panel/*.pyc');
                if os.path.exists(setupPath + '/panel/class/common.py'): public.ExecShell('rm -f ' + setupPath + '/panel/class/*.pyc');
                
                compileall.compile_dir(setupPath + '/panel');
                compileall.compile_dir(setupPath + '/panel/class');
                #if os.path.exists(setupPath + '/panel/main.pyc'):
                    #public.ExecShell('rm -f ' + setupPath + '/panel/class/*.py');
                    #public.ExecShell('rm -f ' + setupPath + '/panel/*.py');
                public.ExecShell('rm -f panel.zip');
                web.ctx.session.version = updateInfo['version']
                return public.returnMsg(True,'PANEL_UPDATE',(updateInfo['version'],));
            
            #输出新版本信息
            data = {
                'status' : True,
                'version': updateInfo['version'],
                'updateMsg' : updateInfo['updateMsg']
            };
            return data;
        except Exception,ex:
            return public.returnMsg(False,"CONNECT_ERR");
         
    #检查是否安装任何
    def CheckInstalled(self,get):
        checks = ['nginx','apache','php','pure-ftpd','mysql'];
        import os,web
        for name in checks:
            filename = web.ctx.session.rootPath + "/server/" + name
            if os.path.exists(filename): return True;
        return False;
    
    
    #取已安装软件列表
    def GetInstalled(self,get):
        import system
        data = system.system().GetConcifInfo()
        return data;
    
    #取PHP配置
    def GetPHPConfig(self,get):
        import web,re,json
        filename = web.ctx.session.setupPath + '/php/' + get.version + '/etc/php.ini'
        if not os.path.exists(filename): return public.returnMsg(False,'PHP_NOT_EXISTS');
        phpini = public.readFile(filename);
        data = {}
        rep = "disable_functions\s*=\s{0,1}(.*)\n"
        tmp = re.search(rep,phpini).groups();
        data['disable_functions'] = tmp[0];
        
        rep = "upload_max_filesize\s*=\s*([0-9]+)M"
        tmp = re.search(rep,phpini).groups()
        data['max'] = tmp[0]
        
        rep = ur"\n;*\s*cgi\.fix_pathinfo\s*=\s*([0-9]+)\s*\n"
        tmp = re.search(rep,phpini).groups()
        if tmp[0] == '0':
            data['pathinfo'] = False
        else:
            data['pathinfo'] = True
        
        phplib = json.loads(public.readFile('data/phplib.conf'));
        libs = [];
        tasks = public.M('tasks').where("status!=?",('1',)).field('status,name').select()
        for lib in phplib:
            lib['task'] = '1';
            for task in tasks:
                tmp = public.getStrBetween('[',']',task['name'])
                if not tmp:continue;
                tmp1 = tmp.split('-');
                if tmp1[0].lower() == lib['name'].lower():
                    lib['task'] = task['status'];
                    lib['phpversions'] = []
                    lib['phpversions'].append(tmp1[1])
            if phpini.find(lib['check']) == -1:
                lib['status'] = False
            else:
                lib['status'] = True
                
            libs.append(lib)
        
        data['libs'] = libs;
        return data
        
        
    #取PHPINFO信息
    def GetPHPInfo(self,get):
        self.CheckPHPINFO();
        sPath = web.ctx.session.setupPath + '/phpinfo/' + get.version;
        if not os.path.exists(sPath + '/phpinfo.php'):
            public.ExecShell("mkdir -p " + sPath);
            public.writeFile(sPath + '/phpinfo.php','<?php phpinfo(); ?>');
        phpinfo = public.httpGet('http://127.0.0.2/' + get.version + '/phpinfo.php');
        return phpinfo;
    
    #检测PHPINFO配置
    def CheckPHPINFO(self):
        php_versions = ['52','53','54','55','56','70','71'];
        path = web.ctx.session.setupPath + '/panel/vhost/nginx/phpinfo.conf';
        if not os.path.exists(path):
            opt = "";
            for version in php_versions:
                opt += "\n\tlocation /"+version+" {\n\t\tinclude enable-php-"+version+".conf;\n\t}";
            
            phpinfoBody = '''server
{
    listen 80;
    server_name 127.0.0.2;
    allow 127.0.0.1;
    index phpinfo.php index.html index.php;
    root  /www/server/phpinfo;
%s   
}''' % (opt,);
            public.writeFile(path,phpinfoBody);
        
        
        path = web.ctx.session.setupPath + '/panel/vhost/apache/phpinfo.conf';
        if not os.path.exists(path):
            opt = "";
            for version in php_versions:
                opt += """\n<Location /%s>
    SetHandler "proxy:unix:/tmp/php-cgi-%s.sock|fcgi://localhost"
</Location>""" % (version,version);
            
            try:
                apacheVersion = public.readFile('/www/server/apache/version.pl').strip();
                if apacheVersion == '2.2': opt = "";
            except:
                pass;
            
            
            phpinfoBody = '''
<VirtualHost *:80>
DocumentRoot "/www/server/phpinfo"
ServerAdmin phpinfo
ServerName 127.0.0.2
%s
<Directory "/www/server/phpinfo">
    SetOutputFilter DEFLATE
    Options FollowSymLinks
    AllowOverride All
    Order allow,deny
    Allow from all
    DirectoryIndex index.php index.html index.htm default.php default.html default.htm
</Directory>
</VirtualHost>
''' % (opt,);
            public.writeFile(path,phpinfoBody);
        public.serviceReload();
            
    
    #清理日志
    def delClose(self,get):
        #return public.returnMsg(False,'演示服务器，禁止此操作!');
        public.M('logs').where('id>?',(0,)).delete();
        public.WriteLog('TYPE_CONFIG','LOG_CLOSE');
        return public.returnMsg(True,'LOG_CLOSE');
    
    #设置PHPMyAdmin
    def setPHPMyAdmin(self,get):
        import re;
        #try:
        if web.ctx.session.webserver == 'nginx':
            filename = web.ctx.session.setupPath + '/nginx/conf/nginx.conf';
        else:
            filename = web.ctx.session.setupPath + '/apache/conf/extra/httpd-vhosts.conf';
        
        conf = public.readFile(filename);
        if hasattr(get,'port'):
            mainPort = public.readFile('data/port.pl').strip();
            if mainPort == get.port:
                return public.returnMsg(False,'SOFT_PHPVERSION_ERR_PORT_RE');
            if web.ctx.session.webserver == 'nginx':
                rep = "listen\s+([0-9]+)\s*;"
                oldPort = re.search(rep,conf).groups()[0];
                conf = re.sub(rep,'listen ' + get.port + ';\n',conf);
            else:
                rep = "Listen\s+([0-9]+)\s*\n";
                oldPort = re.search(rep,conf).groups()[0];
                conf = re.sub(rep,"Listen " + get.port + "\n",conf,1);
                rep = "VirtualHost\s+\*:[0-9]+"
                conf = re.sub(rep,"VirtualHost *:" + get.port,conf,1);
            
            if oldPort == get.port: return public.returnMsg(False,'SOFT_PHPVERSION_ERR_PORT');
            
            public.writeFile(filename,conf);
            import firewalls
            get.ps = public.getMsg('SOFT_PHPVERSION_PS');
            fw = firewalls.firewalls();
            fw.AddAcceptPort(get);           
            public.serviceReload();
            public.WriteLog('TYPE_SOFT','SOFT_PHPMYADMIN_PORT',(get.port,))
            get.id = public.M('firewall').where('port=?',(oldPort,)).getField('id');
            get.port = oldPort;
            fw.DelAcceptPort(get);
            return public.returnMsg(True,'SET_PORT_SUCCESS');
        
        if hasattr(get,'phpversion'):
            if web.ctx.session.webserver == 'nginx':
                filename = web.ctx.session.setupPath + '/nginx/conf/enable-php.conf';
                conf = public.readFile(filename);
                rep = "php-cgi.*\.sock"
                conf = re.sub(rep,'php-cgi-' + get.phpversion + '.sock',conf);
            else:
                rep = "php-cgi.*\.sock"
                conf = re.sub(rep,'php-cgi-' + get.phpversion + '.sock',conf);
                
            public.writeFile(filename,conf);
            public.serviceReload();
            public.WriteLog('TYPE_SOFT','SOFT_PHPMYADMIN_PHP',(get.phpversion,))
            return public.returnMsg(True,'SOFT_PHPVERSION_SET');
        
        if hasattr(get,'password'):
            import panelSite;
            if(get.password == 'close'):
                return panelSite.panelSite().CloseHasPwd(get);
            else:
                return panelSite.panelSite().SetHasPwd(get);
        
        if hasattr(get,'status'):
            if conf.find(web.ctx.session.setupPath + '/stop') != -1:
                conf = conf.replace(web.ctx.session.setupPath + '/stop',web.ctx.session.setupPath + '/phpmyadmin');
                msg = public.getMsg('START')
            else:
                conf = conf.replace(web.ctx.session.setupPath + '/phpmyadmin',web.ctx.session.setupPath + '/stop');
                msg = public.getMsg('STOP')
            
            public.writeFile(filename,conf);
            public.serviceReload();
            public.WriteLog('TYPE_SOFT','SOFT_PHPMYADMIN_STATUS',(msg,))
            return public.returnMsg(True,'SOFT_PHPMYADMIN_STATUS',(msg,));
        #except:
            #return public.returnMsg(False,'ERROR');
            
    def ToPunycode(self,get):
        import re;
        get.domain = get.domain.encode('utf8');
        tmp = get.domain.split('.');
        newdomain = '';
        for dkey in tmp:
                #匹配非ascii字符
                match = re.search(u"[\x80-\xff]+",dkey);
                if not match:
                        newdomain += dkey + '.';
                else:
                        newdomain += 'xn--' + dkey.decode('utf-8').encode('punycode') + '.'

        return newdomain[0:-1];
    
    #保存PHP排序
    def phpSort(self,get):
        if public.writeFile('/www/server/php/sort.pl',get.ssort): return public.returnMsg(True,'SUCCESS');
        return public.returnMsg(False,'ERROR');
    
    #获取广告代码
    def GetAd(self,get):
        try:
            return public.httpGet(web.ctx.session.home + '/Api/GetAD?name='+get.name + '&soc=' + get.soc);
        except:
            return '';
        
    #获取进度
    def GetSpeed(self,get):
        return public.getSpeed();
    
        
        
        