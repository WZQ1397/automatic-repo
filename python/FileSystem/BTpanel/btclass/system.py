#coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板 x3
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2016 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <2879625666@qq.com>
# +-------------------------------------------------------------------
import psutil,web,time,os,public,re
class system:
    setupPath = None;
    
    def __init__(self):
        self.setupPath = web.ctx.session.setupPath;
    
    def GetConcifInfo(self,get=None):
        #取环境配置信息
        if not hasattr(web.ctx.session, 'config'):
            web.ctx.session.config = public.M('config').where("id=?",('1',)).field('webserver,sites_path,backup_path,status,mysql_root').find();
        if not hasattr(web.ctx.session.config,'email'):
            web.ctx.session.config['email'] = public.M('users').where("id=?",('1',)).getField('email');
        data = {}
        data = web.ctx.session.config
        data['webserver'] = web.ctx.session.config['webserver']
        #PHP版本
        phpVersions = ('52','53','54','55','56','70','71','72','73','74')
        
        data['php'] = []
        
        for version in phpVersions:
            tmp = {}
            tmp['setup'] = os.path.exists(self.setupPath + '/php/'+version+'/bin/php');
            if tmp['setup']:
                phpConfig = self.GetPHPConfig(version)
                tmp['version'] = version
                tmp['max'] = phpConfig['max']
                tmp['maxTime'] = phpConfig['maxTime']
                tmp['pathinfo'] = phpConfig['pathinfo']
                tmp['status'] = os.path.exists('/tmp/php-cgi-'+version+'.sock')
                data['php'].append(tmp)
            
        tmp = {}
        data['webserver'] = ''
        serviceName = 'nginx'
        tmp['setup'] = False
        phpversion = "54"
        phpport = '888';
        pstatus = False;
        pauth = False;
        if os.path.exists(self.setupPath+'/nginx'): 
            data['webserver'] = 'nginx'
            serviceName = 'nginx'
            tmp['setup'] = os.path.exists(self.setupPath +'/nginx/sbin/nginx');
            configFile = self.setupPath + '/nginx/conf/nginx.conf';
            try:
                if os.path.exists(configFile):
                    conf = public.readFile(configFile);
                    rep = "listen\s+([0-9]+)\s*;";
                    rtmp = re.search(rep,conf);
                    if rtmp:
                        phpport = rtmp.groups()[0];
                    
                    if conf.find('AUTH_START') != -1: pauth = True;
                    if conf.find(self.setupPath + '/stop') == -1: pstatus = True;
                    configFile = self.setupPath + '/nginx/conf/enable-php.conf';
                    conf = public.readFile(configFile);
                    rep = "php-cgi-([0-9]+)\.sock";
                    rtmp = re.search(rep,conf);
                    if rtmp:
                        phpversion = rtmp.groups()[0];
            except:
                pass;
            
        elif os.path.exists(self.setupPath+'/apache'):
            data['webserver'] = 'apache'
            serviceName = 'httpd'
            tmp['setup'] = os.path.exists(self.setupPath +'/apache/bin/httpd');
            configFile = self.setupPath + '/apache/conf/extra/httpd-vhosts.conf';
            try:
                if os.path.exists(configFile):
                    conf = public.readFile(configFile);
                    rep = "php-cgi-([0-9]+)\.sock";
                    rtmp = re.search(rep,conf);
                    if rtmp:
                        phpversion = rtmp.groups()[0];
                    rep = "Listen\s+([0-9]+)\s*\n";
                    rtmp = re.search(rep,conf);
                    if rtmp:
                        phpport = rtmp.groups()[0];
                    if conf.find('AUTH_START') != -1: pauth = True;
                    if conf.find(self.setupPath + '/stop') == -1: pstatus = True;
            except:
                pass
                
                
        tmp['type'] = data['webserver']
        tmp['version'] = public.readFile(self.setupPath + '/'+data['webserver']+'/version.pl')
        tmp['status'] = False
        result = public.ExecShell('/etc/init.d/' + serviceName + ' status')
        if result[0].find('running') != -1: tmp['status'] = True
        data['web'] = tmp
        
        tmp = {}
        vfile = self.setupPath + '/phpmyadmin/version.pl';
        tmp['version'] = public.readFile(vfile);
        tmp['setup'] = os.path.exists(vfile);
        tmp['status'] = pstatus;
        tmp['phpversion'] = phpversion;
        tmp['port'] = phpport;
        tmp['auth'] = pauth;
        data['phpmyadmin'] = tmp;
        
        tmp = {}
        tmp['setup'] = os.path.exists('/etc/init.d/tomcat');
        tmp['status'] = True
        if public.ExecShell('ps -aux|grep tomcat|grep -v grep')[0] == "": tmp['status'] = False
        tmp['version'] = public.readFile(self.setupPath + '/tomcat/version.pl');
        data['tomcat'] = tmp;
        
        tmp = {}
        tmp['setup'] = os.path.exists(self.setupPath +'/mysql/bin/mysql');
        tmp['version'] = public.readFile(self.setupPath + '/mysql/version.pl')
        tmp['status'] = os.path.exists('/tmp/mysql.sock')
        data['mysql'] = tmp
        
        tmp = {}
        tmp['setup'] = os.path.exists(self.setupPath +'/redis/runtest');
        tmp['status'] = os.path.exists('/var/run/redis_6379.pid');
        data['redis'] = tmp;
        
        tmp = {}
        tmp['setup'] = os.path.exists('/usr/local/memcached/bin/memcached');
        tmp['status'] = os.path.exists('/var/run/memcached.pid');
        data['memcached'] = tmp;
        
        tmp = {}
        tmp['setup'] = os.path.exists(self.setupPath +'/pure-ftpd/bin/pure-pw');
        tmp['version'] = public.readFile(self.setupPath + '/pure-ftpd/version.pl')
        tmp['status'] = os.path.exists('/var/run/pure-ftpd.pid')
        data['pure-ftpd'] = tmp
        data['panel'] = self.GetPanelInfo()
        data['systemdate'] = public.ExecShell('date +"%Y-%m-%d %H:%M:%S %Z %z"')[0];
        
        return data
    
    def GetPanelInfo(self,get=None):
        #取面板配置
        address = public.GetLocalIp()
        try:
            port = web.ctx.host.split(':')[1]
        except:
            port = '80';
        domain = ''
        if os.path.exists('data/domain.conf'):
           domain = public.readFile('data/domain.conf');
        
        autoUpdate = ''
        if os.path.exists('data/autoUpdate.pl'): autoUpdate = 'checked';
        limitip = ''
        if os.path.exists('data/limitip.conf'): limitip = public.readFile('data/limitip.conf');
        
        templates = []
        for template in os.listdir('templates/'):
            if os.path.isdir('templates/' + template): templates.append(template);
        template = public.readFile('data/templates.pl');
        
        check502 = '';
        if os.path.exists('data/502Task.pl'): check502 = 'checked';
        return {'port':port,'address':address,'domain':domain,'auto':autoUpdate,'502':check502,'limitip':limitip,'templates':templates,'template':template}
    
    def GetPHPConfig(self,version):
        #取PHP配置
        file = self.setupPath + "/php/"+version+"/etc/php.ini"
        phpini = public.readFile(file)
        file = self.setupPath + "/php/"+version+"/etc/php-fpm.conf"
        phpfpm = public.readFile(file)
        data = {}
        try:
            rep = "upload_max_filesize\s*=\s*([0-9]+)M"
            tmp = re.search(rep,phpini).groups()
            data['max'] = tmp[0]
        except:
            data['max'] = '50'
        try:
            rep = "request_terminate_timeout\s*=\s*([0-9]+)\n"
            tmp = re.search(rep,phpfpm).groups()
            data['maxTime'] = tmp[0]
        except:
            data['maxTime'] = 0
        
        try:
            rep = ur"\n;*\s*cgi\.fix_pathinfo\s*=\s*([0-9]+)\s*\n"
            tmp = re.search(rep,phpini).groups()
            
            if tmp[0] == '1':
                data['pathinfo'] = True
            else:
                data['pathinfo'] = False
        except:
            data['pathinfo'] = False
        
        return data

    
    def GetSystemTotal(self,get):
        #取系统统计信息
        data = self.GetMemInfo()
        cpu = self.GetCpuInfo()
        data['cpuNum'] = cpu[1]
        data['cpuRealUsed'] = cpu[0]
        data['time'] = self.GetBootTime()
        data['system'] = self.GetSystemVersion();
        data['isuser'] = public.M('users').where('username=?',('admin',)).count();
        return data
    
    def GetSystemVersion(self):
        #取操作系统版本
        import public
        version = public.readFile('/etc/redhat-release')
        if not version:
            version = public.readFile('/etc/issue').replace('\\n \\l','').strip();
        else:
            version = version.replace('release ','').strip();
        return version
    
    def GetBootTime(self):
        #取系统启动时间
        import public,math
        conf = public.readFile('/proc/uptime').split()
        tStr = float(conf[0])
        min = tStr / 60;
        hours = min / 60;
        days = math.floor(hours / 24);
        hours = math.floor(hours - (days * 24));
        min = math.floor(min - (days * 60 * 24) - (hours * 60));
        return public.getMsg('SYS_BOOT_TIME',(str(int(days)),str(int(hours)),str(int(min))))
    
    def GetCpuInfo(self):
        #取CPU信息
        cpuCount = psutil.cpu_count()
        used = psutil.cpu_percent(interval=1)
        return used,cpuCount
    
    def GetMemInfo(self,get=None):
        #取内存信息
        mem = psutil.virtual_memory()
        memInfo = {'memTotal':mem.total/1024/1024,'memFree':mem.free/1024/1024,'memBuffers':mem.buffers/1024/1024,'memCached':mem.cached/1024/1024}
        memInfo['memRealUsed'] = memInfo['memTotal'] - memInfo['memFree'] - memInfo['memBuffers'] - memInfo['memCached']
        return memInfo
    
    def GetDiskInfo(self,get=None):
        return self.GetDiskInfo2();
        #取磁盘分区信息
        diskIo = psutil.disk_partitions()
        diskInfo = []
        
        for disk in diskIo:
            if disk[1] == '/mnt/cdrom':continue;
            if disk[1] == '/boot':continue;
            tmp = {}
            tmp['path'] = disk[1]
            tmp['size'] = psutil.disk_usage(disk[1])
            diskInfo.append(tmp)
        return diskInfo
    
    def GetDiskInfo2(self):
        #取磁盘分区信息
        temp = public.ExecShell("df -h -P|grep '/'|grep -v tmpfs")[0];
        temp1 = temp.split('\n');
        diskInfo = [];
        cuts = ['/mnt/cdrom','/boot','/boot/efi','/dev','/dev/shm'];
        for tmp in temp1:
            disk = tmp.split();
            if len(disk) < 5: continue;
            if disk[1].find('M') != -1: continue;
            if len(disk[5].split('/')) > 4: continue;
            if disk[5] in cuts: continue;
            arr = {}
            arr['path'] = disk[5];
            tmp1 = [disk[1],disk[2],disk[3],disk[4]];
            arr['size'] = tmp1;
            diskInfo.append(arr);
        return diskInfo
    
    def GetNetWork(self,get=None):
        #取网络流量信息
        try:
            networkIo = psutil.net_io_counters()[:4]
            if not hasattr(web.ctx.session,'otime'):
                web.ctx.session.up   =  networkIo[0]
                web.ctx.session.down =  networkIo[1]
                web.ctx.session.otime = time.time();
            
            ntime = time.time();
            networkInfo = {}
            networkInfo['upTotal']   = networkIo[0]
            networkInfo['downTotal'] = networkIo[1]
            networkInfo['up']        = round(float(networkIo[0] - web.ctx.session.up) / 1024 / (ntime - web.ctx.session.otime),2)
            networkInfo['down']      = round(float(networkIo[1] - web.ctx.session.down) / 1024 / (ntime - web.ctx.session.otime),2)
            networkInfo['downPackets'] =networkIo[3]
            networkInfo['upPackets']   =networkIo[2]
            
            web.ctx.session.up   =  networkIo[0]
            web.ctx.session.down =  networkIo[1]
            web.ctx.session.otime = ntime;
            
            networkInfo['cpu'] = self.GetCpuInfo()
            return networkInfo
        except:
            return None
    
    def GetNetWorkOld(self):
        #取网络流量信息
        import time;
        pnet = public.readFile('/proc/net/dev');
        rep = '([^\s]+):[\s]{0,}(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)';
        pnetall = re.findall(rep,pnet);
        networkInfo = {}
        networkInfo['upTotal'] = networkInfo['downTotal'] = networkInfo['up'] = networkInfo['down'] = networkInfo['downPackets'] = networkInfo['upPackets'] = 0;
        for pnetInfo in pnetall:
            if pnetInfo[0] == 'io': continue;
            networkInfo['downTotal'] += int(pnetInfo[1]);
            networkInfo['downPackets'] += int(pnetInfo[2]);
            networkInfo['upTotal'] += int(pnetInfo[9]);
            networkInfo['upPackets'] += int(pnetInfo[10]);
        
        if not hasattr(web.ctx.session,'otime'):
            web.ctx.session.up   =  networkInfo['upTotal']
            web.ctx.session.down =  networkInfo['downTotal']
            web.ctx.session.otime = time.time();
        ntime = time.time();
        tmpDown = networkInfo['downTotal'] - web.ctx.session.down;
        tmpUp = networkInfo['upTotal'] - web.ctx.session.up;
        networkInfo['down'] = str(round(float(tmpDown) / 1024 / (ntime - web.ctx.session.otime),2));
        networkInfo['up']   = str(round(float(tmpUp) / 1024 / (ntime - web.ctx.session.otime),2));
        if networkInfo['down'] < 0: networkInfo['down'] = 0;
        if networkInfo['up'] < 0: networkInfo['up'] = 0;
        
        web.ctx.session.up   =  networkInfo['upTotal'];
        web.ctx.session.down =  networkInfo['downTotal'];
        web.ctx.session.otime = ntime;
        networkInfo['cpu'] = self.GetCpuInfo()
        return networkInfo;
    
    def ServiceAdmin(self,get=None):
        #服务管理
        
        if get.name == 'mysqld': public.CheckMyCnf();
        
        if get.name == 'phpmyadmin':
            import ajax
            get.status = 'True';
            ajax.ajax().setPHPMyAdmin(get);
        
        #检查httpd配置文件
        if get.name == 'apache' or get.name == 'httpd':
            get.name = 'httpd';
            if not os.path.exists(self.setupPath+'/apache/bin/apachectl'): return public.returnMsg(True,'SYS_NOT_INSTALL_APACHE');
            vhostPath = self.setupPath + '/panel/vhost/apache'
            if not os.path.exists(vhostPath):
                public.ExecShell('mkdir ' + vhostPath);
                public.ExecShell('/etc/init.d/httpd start');
            result = public.ExecShell(self.setupPath+'/apache/bin/apachectl -t');
            if result[1].find('Syntax OK') == -1:
                public.WriteLog("TYPE_SOFT",'SYS_EXEC_ERR', (str(result),));
                return public.returnMsg(False,'SYS_CONF_APACHE_ERR',(result[1].replace("\n",'<br>'),));
        #检查nginx配置文件
        elif get.name == 'nginx':
            vhostPath = self.setupPath + '/panel/vhost/rewrite'
            if not os.path.exists(vhostPath): public.ExecShell('mkdir ' + vhostPath);
            vhostPath = self.setupPath + '/panel/vhost/nginx'
            if not os.path.exists(vhostPath):
                public.ExecShell('mkdir ' + vhostPath);
                public.ExecShell('/etc/init.d/nginx start');
            
            result = public.ExecShell('nginx -t -c '+self.setupPath+'/nginx/conf/nginx.conf');
            if result[1].find('perserver') != -1:
                limit = self.setupPath + '/nginx/conf/nginx.conf';
                nginxConf = public.readFile(limit);
                limitConf = "limit_conn_zone $binary_remote_addr zone=perip:10m;\n\t\tlimit_conn_zone $server_name zone=perserver:10m;";
                nginxConf = nginxConf.replace("#limit_conn_zone $binary_remote_addr zone=perip:10m;",limitConf);
                public.writeFile(limit,nginxConf)
                public.ExecShell('/etc/init.d/nginx start');
                return public.returnMsg(True,'SYS_CONF_NGINX_REP');
            
            if result[1].find('proxy') != -1:
                import panelSite
                panelSite.panelSite().CheckProxy(get);
                public.ExecShell('/etc/init.d/nginx start');
                return public.returnMsg(True,'SYS_CONF_NGINX_REP');
            
            #return result
            if result[1].find('successful') == -1:
                public.WriteLog("TYPE_SOFT",'SYS_EXEC_ERR', (str(result),));
                return public.returnMsg(False,'SYS_CONF_NGINX_ERR',(result[1].replace("\n",'<br>'),));
        
        #执行
        execStr = "/etc/init.d/"+get.name+" "+get.type
        if execStr == '/etc/init.d/pure-ftpd reload': execStr = self.setupPath+'/pure-ftpd/bin/pure-pw mkdb '+self.setupPath+'/pure-ftpd/etc/pureftpd.pdb'
        if execStr == '/etc/init.d/pure-ftpd start': os.system('pkill -9 pure-ftpd');
        if execStr == '/etc/init.d/tomcat reload': execStr = '/etc/init.d/tomcat stop && /etc/init.d/tomcat start';
        if execStr == '/etc/init.d/tomcat restart': execStr = '/etc/init.d/tomcat stop && /etc/init.d/tomcat start';
        
        if get.name != 'nginx':
            os.system(execStr);
            return public.returnMsg(True,'SYS_EXEC_SUCCESS');
        result = public.ExecShell(execStr)
        if result[1].find('nginx.pid') != -1:
            public.ExecShell('pkill -9 nginx && sleep 1');
            public.ExecShell('/etc/init.d/nginx start');
        if get.type != 'test':
            public.WriteLog("TYPE_SOFT", 'SYS_EXEC_SUCCESS',(execStr,));
        return public.returnMsg(True,'SYS_EXEC_SUCCESS');
    
    def RestartServer(self,get):
        if not public.IsRestart(): return public.returnMsg(False,'EXEC_ERR_TASK');
        public.ExecShell("sync && /etc/init.d/bt stop && init 6 &");
        return public.returnMsg(True,'SYS_REBOOT');
    
    #释放内存
    def ReMemory(self,get):
        os.system('sync');
        scriptFile = 'script/rememory.sh'
        if not os.path.exists(scriptFile):
            public.downloadFile(web.ctx.session.home + '/script/rememory.sh',scriptFile);
        public.ExecShell("/bin/bash " + self.setupPath + '/panel/' + scriptFile);
        return self.GetMemInfo();
    
    #重启面板     
    def ReWeb(self,get):
        #if not public.IsRestart(): return public.returnMsg(False,'EXEC_ERR_TASK');
        public.ExecShell('/etc/init.d/bt restart &')
        return True
    
    #修复面板
    def RepPanel(self,get):
        public.ExecShell("wget -O update.sh http://download.bt.cn/install/update.sh && sh update.sh " + web.ctx.session.version);
        return True;
        
        
        
        
        
        