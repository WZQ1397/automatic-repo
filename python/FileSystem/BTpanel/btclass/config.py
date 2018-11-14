#coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板 x3
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2017 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <2879625666@qq.com>
# +-------------------------------------------------------------------

import public,web,re,sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
class config:
    
    def setPassword(self,get):
        #return public.returnMsg(False,'体验服务器，禁止修改!')
        if get.password1 != get.password2: return public.returnMsg(False,'USER_PASSWORD_CHECK')
        if len(get.password1) < 5: return public.returnMsg(False,'USER_PASSWORD_LEN')
        public.M('users').where("username=?",(web.ctx.session.username,)).setField('password',public.md5(get.password1.strip()))
        public.WriteLog('TYPE_PANEL','USER_PASSWORD_SUCCESS',(web.ctx.session.username,))
        return public.returnMsg(True,'USER_PASSWORD_SUCCESS')
    
    def setUsername(self,get):
        #return public.returnMsg(False,'体验服务器，禁止修改!')
        if get.username1 != get.username2: return public.returnMsg(False,'USER_USERNAME_CHECK')
        if len(get.username1) < 3: return public.returnMsg(False,'USER_USERNAME_LEN')
        public.M('users').where("username=?",(web.ctx.session.username,)).setField('username',get.username1.strip())
        web.ctx.session.username = get.username1
        public.WriteLog('TYPE_PANEL','USER_USERNAME_SUCCESS',(get.username1,get.username2))
        return public.returnMsg(True,'USER_USERNAME_SUCCESS')
    
    def setPanel(self,get):
        #return public.returnMsg(False,'体验服务器，禁止修改!')
        if not public.IsRestart(): return public.returnMsg(False,'EXEC_ERR_TASK');
        if get.domain:
            reg = "^([\w\-\*]{1,100}\.){1,4}(\w{1,10}|\w{1,10}\.\w{1,10})$";
            if not re.match(reg, get.domain): return public.returnMsg(False,'SITE_ADD_ERR_DOMAIN');
        isReWeb = False
        oldPort = web.ctx.host.split(':')[1];
        newPort = get.port;
        if oldPort != get.port:
            if self.IsOpen(get.port):
                return public.returnMsg(False,'PORT_CHECK_EXISTS',(get,port,))
            if int(get.port) >= 65535 or  int(get.port) < 100: return public.returnMsg(False,'PORT_CHECK_RANGE');
            public.writeFile('data/port.pl',get.port)
            import firewalls
            get.ps = public.getMsg('PORT_CHECK_PS');
            fw = firewalls.firewalls();
            fw.AddAcceptPort(get);
            get.port = oldPort;
            get.id = public.M('firewall').where("port=?",(oldPort,)).getField('id');
            fw.DelAcceptPort(get);
            isReWeb = True
        
        if get.webname != web.ctx.session.webname: 
            web.ctx.session.webname = get.webname
            public.writeFile('data/title.pl',get.webname);
        
        limitip = public.readFile('data/limitip.conf');
        if get.limitip != limitip: public.writeFile('data/limitip.conf',get.limitip);
        
        public.writeFile('data/domain.conf',get.domain.strip())
        public.writeFile('data/iplist.txt',get.address)
        
        public.M('config').where("id=?",('1',)).save('backup_path,sites_path',(get.backup_path,get.sites_path))
        web.ctx.session.config['backup_path'] = get.backup_path
        web.ctx.session.config['sites_path'] = get.sites_path
        
        data = {'uri':web.ctx.fullpath,'host':web.ctx.host.split(':')[0]+':'+newPort,'status':True,'isReWeb':isReWeb,'msg':public.getMsg('PANEL_SAVE')}
        public.WriteLog('TYPE_PANEL','PANEL_SAVE',(newPort,get.domain,get.backup_path,get.sites_path,get.address,get.limitip))
        return data
    
    def setPathInfo(self,get):
        #设置PATH_INFO
        version = get.version
        type = get.type
        if web.ctx.session.webserver == 'nginx':
            path = web.ctx.session.setupPath+'/nginx/conf/enable-php-'+version+'.conf';
            conf = public.readFile(path);
            rep = "\s+#*include\s+pathinfo.conf;";
            if type == 'on':
                conf = re.sub(rep,'\n\t\t\tinclude pathinfo.conf;',conf)
            else:
                conf = re.sub(rep,'\n\t\t\t#include pathinfo.conf;',conf)
            public.writeFile(path,conf)
            public.serviceReload();
        
        path = web.ctx.session.setupPath+'/php/'+version+'/etc/php.ini';
        conf = public.readFile(path);
        rep = "\n*\s*cgi\.fix_pathinfo\s*=\s*([0-9]+)\s*\n";
        status = '0'
        if type == 'on':status = '1'
        conf = re.sub(rep,"\ncgi.fix_pathinfo = "+status+"\n",conf)
        public.writeFile(path,conf)
        public.WriteLog("TYPE_PHP", "PHP_PATHINFO_SUCCESS",(version,type));
        public.phpReload(version);
        return public.returnMsg(True,'SET_SUCCESS');
    
    
    #设置文件上传大小限制
    def setPHPMaxSize(self,get):
        version = get.version
        max = get.max
        
        if int(max) < 2: return public.returnMsg(False,'PHP_UPLOAD_MAX_ERR')
        
        #设置PHP
        path = web.ctx.session.setupPath+'/php/'+version+'/etc/php.ini'
        conf = public.readFile(path)
        rep = u"\nupload_max_filesize\s*=\s*[0-9]+M"
        conf = re.sub(rep,u'\nupload_max_filesize = '+max+'M',conf)
        rep = u"\npost_max_size\s*=\s*[0-9]+M"
        conf = re.sub(rep,u'\npost_max_size = '+max+'M',conf)
        public.writeFile(path,conf)
        
        if web.ctx.session.webserver == 'nginx':
            #设置Nginx
            path = web.ctx.session.setupPath+'/nginx/conf/nginx.conf'
            conf = public.readFile(path)
            rep = "client_max_body_size\s+([0-9]+)m"
            tmp = re.search(rep,conf).groups()
            if int(tmp[0]) < int(max):
                conf = re.sub(rep,'client_max_body_size '+max+'m',conf)
                public.writeFile(path,conf)
            
        public.serviceReload()
        public.phpReload(version);
        public.WriteLog("TYPE_PHP", "PHP_UPLOAD_MAX",(version,max))
        return public.returnMsg(True,'SET_SUCCESS')
    
    #设置禁用函数
    def setPHPDisable(self,get):
        filename = web.ctx.session.setupPath + '/php/' + get.version + '/etc/php.ini'
        if not os.path.exists(filename): return public.returnMsg(False,'PHP_NOT_EXISTS');
        phpini = public.readFile(filename);
        rep = "disable_functions\s*=\s*.*\n"
        phpini = re.sub(rep, 'disable_functions = ' + get.disable_functions + "\n", phpini);
        public.WriteLog('TYPE_PHP','PHP_DISABLE_FUNCTION',(get.version,get.disable_functions))
        public.writeFile(filename,phpini);
        public.phpReload(get.version);
        return public.returnMsg(True,'SET_SUCCESS');
    
    #设置PHP超时时间
    def setPHPMaxTime(self,get):
        time = get.time
        version = get.version;
        if int(time) < 30 or int(time) > 86400: return public.returnMsg(False,'PHP_TIMEOUT_ERR');
        file = web.ctx.session.setupPath+'/php/'+version+'/etc/php-fpm.conf';
        conf = public.readFile(file);
        rep = "request_terminate_timeout\s*=\s*([0-9]+)\n";
        conf = re.sub(rep,"request_terminate_timeout = "+time+"\n",conf);    
        public.writeFile(file,conf)
        
        file = '/www/server/php/'+version+'/etc/php.ini';
        phpini = public.readFile(file);
        rep = "max_execution_time\s*=\s*([0-9]+)\r?\n";
        phpini = re.sub(rep,"max_execution_time = "+time+"\n",phpini);
        rep = "max_input_time\s*=\s*([0-9]+)\r?\n";
        phpini = re.sub(rep,"max_input_time = "+time+"\n",phpini);
        public.writeFile(file,phpini)
        
        if web.ctx.session.webserver == 'nginx':
            #设置Nginx
            path = web.ctx.session.setupPath+'/nginx/conf/nginx.conf';
            conf = public.readFile(path);
            rep = "fastcgi_connect_timeout\s+([0-9]+);";
            tmp = re.search(rep, conf).groups();
            if int(tmp[0]) < time:
                conf = re.sub(rep,'fastcgi_connect_timeout '+time+';',conf);
                rep = "fastcgi_send_timeout\s+([0-9]+);";
                conf = re.sub(rep,'fastcgi_send_timeout '+time+';',conf);
                rep = "fastcgi_read_timeout\s+([0-9]+);";
                conf = re.sub(rep,'fastcgi_read_timeout '+time+';',conf);
                public.writeFile(path,conf);
                
        public.WriteLog("TYPE_PHP", "PHP_TIMEOUT",(version,time));
        public.serviceReload()
        public.phpReload(version);
        return public.returnMsg(True, 'SET_SUCCESS');
    
    
    #取FPM设置
    def getFpmConfig(self,get):
        version = get.version;
        file = web.ctx.session.setupPath+"/php/"+version+"/etc/php-fpm.conf";
        conf = public.readFile(file);
        data = {}
        rep = "\s*pm.max_children\s*=\s*([0-9]+)\s*";
        tmp = re.search(rep, conf).groups();
        data['max_children'] = tmp[0];
        
        rep = "\s*pm.start_servers\s*=\s*([0-9]+)\s*";
        tmp = re.search(rep, conf).groups();
        data['start_servers'] = tmp[0];
        
        rep = "\s*pm.min_spare_servers\s*=\s*([0-9]+)\s*";
        tmp = re.search(rep, conf).groups();
        data['min_spare_servers'] = tmp[0];
        
        rep = "\s*pm.max_spare_servers \s*=\s*([0-9]+)\s*";
        tmp = re.search(rep, conf).groups();
        data['max_spare_servers'] = tmp[0];
        
        rep = "\s*pm\s*=\s*(\w+)\s*";
        tmp = re.search(rep, conf).groups();
        data['pm'] = tmp[0];
        
        return data


    #设置
    def setFpmConfig(self,get):
        version = get.version
        max_children = get.max_children
        start_servers = get.start_servers
        min_spare_servers = get.min_spare_servers
        max_spare_servers = get.max_spare_servers
        pm = get.pm
        
        file = web.ctx.session.setupPath+"/php/"+version+"/etc/php-fpm.conf";
        conf = public.readFile(file);
        
        rep = "\s*pm.max_children\s*=\s*([0-9]+)\s*";
        conf = re.sub(rep, "\npm.max_children = "+max_children, conf);
        
        rep = "\s*pm.start_servers\s*=\s*([0-9]+)\s*";
        conf = re.sub(rep, "\npm.start_servers = "+start_servers, conf);
        
        rep = "\s*pm.min_spare_servers\s*=\s*([0-9]+)\s*";
        conf = re.sub(rep, "\npm.min_spare_servers = "+min_spare_servers, conf);
        
        rep = "\s*pm.max_spare_servers \s*=\s*([0-9]+)\s*";
        conf = re.sub(rep, "\npm.max_spare_servers = "+max_spare_servers+"\n", conf);
        
        rep = "\s*pm\s*=\s*(\w+)\s*";
        conf = re.sub(rep, "\npm = "+pm+"\n", conf);
        
        public.writeFile(file,conf)
        public.phpReload(version);
        public.WriteLog("TYPE_PHP",'PHP_CHILDREN', (version,max_children,start_servers,min_spare_servers,max_spare_servers));
        return public.returnMsg(True, 'SET_SUCCESS');
    
    #同步时间
    def syncDate(self,get):
        result = public.ExecShell("ntpdate 0.asia.pool.ntp.org");
        public.WriteLog("TYPE_PANEL", "DATE_SUCCESS");
        return public.returnMsg(True,"DATE_SUCCESS");
        
    def IsOpen(self,port):
        #检查端口是否占用
        import socket
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect(('127.0.0.1',int(port)))
            s.shutdown(2)
            return True
        except:
            return False
    
    #设置是否开启监控
    def SetControl(self,get):
        try:
            if hasattr(get,'day'): 
                get.day = int(get.day);
                get.day = str(get.day);
                if(get.day < 1): return public.returnMsg(False,"CONTROL_ERR");
        except:
            pass
        
        filename = 'data/control.conf';
        if get.type == '1':
            public.writeFile(filename,get.day);
            public.WriteLog("TYPE_PANEL",'CONTROL_OPEN',(get.day,));
        elif get.type == '0':
            public.ExecShell("rm -f " + filename);
            public.WriteLog("TYPE_PANEL", "CONTROL_CLOSE");
        elif get.type == 'del':
            if not public.IsRestart(): return public.returnMsg(False,'EXEC_ERR_TASK');
            os.remove("data/system.db")
            import db;
            sql = db.Sql()
            result = sql.dbfile('system').create('system');
            public.WriteLog("TYPE_PANEL", "CONTROL_CLOSE");
            return public.returnMsg(True,"CONTROL_CLOSE");
            
        else:
            data = {}
            if os.path.exists(filename):
                try:
                    data['day'] = int(public.readFile(filename));
                except:
                    data['day'] = 30;
                data['status'] = True
            else:
                data['day'] = 30;
                data['status'] = False
            return data
        
        return public.returnMsg(True,"SET_SUCCESS");
    
    #关闭面板
    def ClosePanel(self,get):
        #return public.returnMsg(False,'体验服务器，禁止修改!')
        filename = 'data/close.pl'
        public.writeFile(filename,'True');
        public.ExecShell("chmod 600 " + filename);
        public.ExecShell("chown root.root " + filename);
        return public.returnMsg(True,'PANEL_CLOSE');
    
    
    #设置自动更新
    def AutoUpdatePanel(self,get):
        #return public.returnMsg(False,'体验服务器，禁止修改!')
        filename = 'data/autoUpdate.pl'
        if os.path.exists(filename):
            os.remove(filename);
        else:
            public.writeFile(filename,'True');
            public.ExecShell("chmod 600 " + filename);
            public.ExecShell("chown root.root " + filename);
        return public.returnMsg(True,'SET_SUCCESS');
    
    #设置二级密码
    def SetPanelLock(self,get):
        path = 'data/lock';
        if not os.path.exists(path):
            public.ExecShell('mkdir ' + path);
            public.ExecShell("chmod 600 " + path);
            public.ExecShell("chown root.root " + path);
        
        keys = ['files','tasks','config'];
        for name in keys:
            filename = path + '/' + name + '.pl';
            if hasattr(get,name):
                public.writeFile(filename,'True');
            else:
                if os.path.exists(filename): os.remove(filename);
                
    #设置PHP守护程序
    def Set502(self,get):
        filename = 'data/502Task.pl';
        if os.path.exists(filename):
            os.system('rm -f ' + filename)
        else:
            public.writeFile(filename,'True')
        
        return public.returnMsg(True,'SET_SUCCESS');
    
    #设置模板
    def SetTemplates(self,get):
        public.writeFile('data/templates.pl',get.templates);
        return public.returnMsg(True,'SET_SUCCESS');
    
    #设置面板SSL
    def SetPanelSSL(self,get):
        sslConf = '/www/server/panel/data/ssl.pl';
        if os.path.exists(sslConf):
            os.system('rm -f ' + sslConf);
            return public.returnMsg(True,'PANEL_SSL_CLOSE');
        else:
            os.system('pip install pyOpenSSL');
            try:
                if not self.CreateSSL(): return public.returnMsg(False,'PANEL_SSL_ERR');
                public.writeFile(sslConf,'True')
            except Exception,ex:
                return public.returnMsg(False,'PANEL_SSL_ERR');
            return public.returnMsg(True,'PANEL_SSL_OPEN');
    #自签证书
    def CreateSSL(self):
        import OpenSSL
        key = OpenSSL.crypto.PKey()
        key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
        cert = OpenSSL.crypto.X509()
        cert.set_serial_number(0)
        cert.get_subject().CN = public.GetLocalIp();
        cert.set_issuer(cert.get_subject())
        cert.gmtime_adj_notBefore( 0 )
        cert.gmtime_adj_notAfter(86400 * 3650)
        cert.set_pubkey( key )
        cert.sign( key, 'md5' )
        cert_ca = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        private_key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
        if len(cert_ca) > 100 and len(private_key) > 100:
            public.writeFile('ssl/certificate.pem',cert_ca)
            public.writeFile('ssl/privateKey.pem',private_key)
            return True
        return False
        
    #生成Token
    def SetToken(self,get):
        data = {}
        data[''] = public.GetRandomString(24);
    
    #取面板列表
    def GetPanelList(self,get):
        try:
            data = public.M('panel').field('id,title,url,username,password,click,addtime').order('click desc').select();
            if type(data) == str: data[111111];
            return data;
        except:
            sql = '''CREATE TABLE IF NOT EXISTS `panel` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `title` TEXT,
  `url` TEXT,
  `username` TEXT,
  `password` TEXT,
  `click` INTEGER,
  `addtime` INTEGER
);'''
            public.M('sites').execute(sql,());
            return [];
    
    #添加面板资料
    def AddPanelInfo(self,get):
        
        #校验是还是重复
        isAdd = public.M('panel').where('title=? OR url=?',(get.title,get.url)).count();
        if isAdd: return public.returnMsg(False,'PANEL_SSL_ADD_EXISTS');
        import time,json;
        isRe = public.M('panel').add('title,url,username,password,click,addtime',(get.title,get.url,get.username,get.password,0,int(time.time())));
        if isRe: return public.returnMsg(True,'ADD_SUCCESS');
        return public.returnMsg(False,'ADD_ERROR');
    
    #修改面板资料
    def SetPanelInfo(self,get):
        #校验是还是重复
        isSave = public.M('panel').where('(title=? OR url=?) AND id!=?',(get.title,get.url,get.id)).count();
        if isSave: return public.returnMsg(False,'PANEL_SSL_ADD_EXISTS');
        import time,json;
        
        #更新到数据库
        isRe = public.M('panel').where('id=?',(get.id,)).save('title,url,username,password',(get.title,get.url,get.username,get.password));
        if isRe: return public.returnMsg(True,'EDIT_SUCCESS');
        return public.returnMsg(False,'EDIT_ERROR');
        pass
    
    #删除面板资料
    def DelPanelInfo(self,get):
        isExists = public.M('panel').where('id=?',(get.id,)).count();
        if not isExists: return public.returnMsg(False,'PANEL_SSL_ADD_NOT_EXISTS');
        public.M('panel').where('id=?',(get.id,)).delete();
        return public.returnMsg(True,'DEL_SUCCESS');
        pass 
    
    #点击计数
    def ClickPanelInfo(self,get):
        click = public.M('panel').where('id=?',(get.id,)).getField('click');
        public.M('panel').where('id=?',(get.id,)).setField('click',click+1);
        return True;
    
    #获取PHP配置参数
    def GetPHPConf(self,get):
        gets = [
                {'name':'short_open_tag','type':1,'ps':public.getMsg('PHP_CONF_1')},
                {'name':'asp_tags','type':1,'ps':public.getMsg('PHP_CONF_2')},
                {'name':'safe_mode','type':1,'ps':public.getMsg('PHP_CONF_3')},
                {'name':'max_execution_time','type':2,'ps':public.getMsg('PHP_CONF_4')},
                {'name':'max_input_time','type':2,'ps':public.getMsg('PHP_CONF_5')},
                {'name':'memory_limit','type':2,'ps':public.getMsg('PHP_CONF_6')},
                {'name':'post_max_size','type':2,'ps':public.getMsg('PHP_CONF_7')},
                {'name':'file_uploads','type':1,'ps':public.getMsg('PHP_CONF_8')},
                {'name':'upload_max_filesize','type':2,'ps':public.getMsg('PHP_CONF_9')},
                {'name':'max_file_uploads','type':2,'ps':public.getMsg('PHP_CONF_10')},
                {'name':'default_socket_timeout','type':2,'ps':public.getMsg('PHP_CONF_11')},
                {'name':'error_reporting','type':3,'ps':public.getMsg('PHP_CONF_12')},
                {'name':'display_errors','type':1,'ps':public.getMsg('PHP_CONF_13')},
                {'name':'cgi.fix_pathinfo','type':0,'ps':public.getMsg('PHP_CONF_14')},
                {'name':'date.timezone','type':3,'ps':public.getMsg('PHP_CONF_15')}
                ]
        phpini = public.readFile('/www/server/php/' + get.version + '/etc/php.ini');
        
        result = []
        for g in gets:
            rep = g['name'] + '\s*=\s*([0-9A-Za-z_& ~]+)(\s*;?|\r?\n)';
            tmp = re.search(rep,phpini)
            if not tmp: continue;
            g['value'] = tmp.groups()[0];
            result.append(g);
        
        return result;
    
    #提交PHP配置参数
    def SetPHPConf(self,get):
        gets = ['display_errors','cgi.fix_pathinfo','date.timezone','short_open_tag','asp_tags','safe_mode','max_execution_time','max_input_time','memory_limit','post_max_size','file_uploads','upload_max_filesize','max_file_uploads','default_socket_timeout','error_reporting']
        
        filename = '/www/server/php/' + get.version + '/etc/php.ini';
        phpini = public.readFile(filename);
        for g in gets:
            rep = g + '\s*=\s*(.+)\r?\n';
            val = g+' = ' + get[g] + '\n';
            phpini = re.sub(rep,val,phpini);
        
        public.writeFile(filename,phpini);
        os.system('/etc/init.d/php-fpm-' + get.version + ' reload');
        return public.returnMsg(True,'SET_SUCCESS');
        
        
            
       
        