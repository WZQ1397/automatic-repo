#coding: utf-8
#-------------------------------------------------------------------
# 宝塔Linux面板
#-------------------------------------------------------------------
# Copyright (c) 2015-2016 宝塔软件(http:#bt.cn) All rights reserved.
#-------------------------------------------------------------------
# Author: 黄文良 <2879625666@qq.com>
#-------------------------------------------------------------------

#------------------------------
# 网站管理类
#------------------------------
import io,re,public,os,web,sys
reload(sys)
sys.setdefaultencoding('utf-8')
class panelSite:
    siteName = None #网站名称
    sitePath = None #根目录
    sitePort = None #端口
    phpVersion = None #PHP版本
    setupPath = None #安装路径
    isWriteLogs = None #是否写日志
    
    def __init__(self):
        self.setupPath = '/www/server';
        path = self.setupPath + '/panel/vhost/nginx'
        if not os.path.exists(path): public.ExecShell("mkdir -p " + path + " && chmod -R 644 " + path)
        path = self.setupPath + '/panel/vhost/apache'
        if not os.path.exists(path): public.ExecShell("mkdir -p " + path + " && chmod -R 644 " + path)
        path = self.setupPath + '/panel/vhost/rewrite'
        if not os.path.exists(path): public.ExecShell("mkdir -p " + path + " && chmod -R 644 " + path)
        path = self.setupPath + '/stop';
        if not os.path.exists(path):
            os.system('mkdir -p ' + path)
            os.system('wget -O ' + path + '/index.html '+public.get_url()+'/stop.html &');
        self.OldConfigFile();
    
    #添加apache端口
    def apacheAddPort(self,port):
        filename = self.setupPath+'/apache/conf/httpd.conf';
        if not os.path.exists(filename): return;
        allConf = public.readFile(filename);
        rep = "Listen\s+([0-9]+)\n";
        tmp = re.findall(rep,allConf);
        
        for key in tmp:
            if key == port: return False
        
        listen = "\nListen "+tmp[0]
        allConf = allConf.replace(listen,listen + "\nListen " + port)
        public.writeFile(filename, allConf)
        return True
    
    #添加到apache
    def apacheAdd(self):
        import time
        listen = '';
        if self.sitePort != '80': self.apacheAddPort(self.sitePort);
        acc = public.md5(str(time.time()))[0:8];
        try:
            httpdVersion = public.readFile(self.setupPath+'/apache/version.pl').strip();
        except:
            httpdVersion = "";
        if httpdVersion == '2.2':
            vName = "NameVirtualHost  *:"+self.sitePort+"\n";
            phpConfig = "";
            apaOpt = "Order allow,deny\n\t\tAllow from all";
        else:
            vName = "";
            phpConfig ='''
    #PHP
    <FilesMatch \\.php$>
            SetHandler "proxy:unix:/tmp/php-cgi-%s.sock|fcgi://localhost"
    </FilesMatch>
    ''' % (self.phpVersion,)
            apaOpt = 'Require all granted';
        
        conf='''%s<VirtualHost *:%s>
    ServerAdmin webmaster@example.com
    DocumentRoot "%s"
    ServerName %s.%s
    ServerAlias %s
    errorDocument 404 /404.html
    ErrorLog "%s-error_log"
    CustomLog "%s-access_log" combined
    %s
    #PATH
    <Directory "%s">
        SetOutputFilter DEFLATE
        Options FollowSymLinks
        AllowOverride All
        %s
        DirectoryIndex index.php index.html index.htm default.php default.html default.htm
    </Directory>
</VirtualHost>''' % (vName,self.sitePort,self.sitePath,acc,self.siteName,self.siteName,web.ctx.session.logsPath+'/'+self.siteName,web.ctx.session.logsPath+'/'+self.siteName,phpConfig,self.sitePath,apaOpt)
    
        if not os.path.exists(self.sitePath+'/.htaccess'): public.writeFile(self.sitePath+'/.htaccess', ' ');
        filename = self.setupPath+'/panel/vhost/apache/'+self.siteName+'.conf'
        public.writeFile(filename,conf)
        return True
        pass
    
    #添加到nginx
    def nginxAdd(self):
        conf='''server
{
    listen %s;
    server_name %s;
    index index.php index.html index.htm default.php default.htm default.html;
    root %s;
    
    #SSL-START %s
    #error_page 404/404.html;
    #SSL-END
    
    #ERROR-PAGE-START  %s
    error_page 404 /404.html;
    error_page 502 /502.html;
    #ERROR-PAGE-END
    
    #PHP-INFO-START  %s
    include enable-php-%s.conf;
    #PHP-INFO-END
    
    #REWRITE-START %s
    include %s/panel/vhost/rewrite/%s.conf;
    #REWRITE-END
    
    location ~ .*\\.(gif|jpg|jpeg|png|bmp|swf)$
    {
        expires      30d;
        access_log off; 
    }
    
    location ~ .*\\.(js|css)?$
    {
        expires      12h;
        access_log off; 
    }
    access_log  %s.log;
}''' % (self.sitePort,self.siteName,self.sitePath,public.getMsg('NGINX_CONF_MSG1'),public.getMsg('NGINX_CONF_MSG2'),public.getMsg('NGINX_CONF_MSG3'),self.phpVersion,public.getMsg('NGINX_CONF_MSG4'),self.setupPath,self.siteName,web.ctx.session.logsPath+'/'+self.siteName)
        
        #写配置文件
        filename = self.setupPath+'/panel/vhost/nginx/'+self.siteName+'.conf'
        public.writeFile(filename,conf);
        
        #生成伪静态文件
        urlrewritePath = self.setupPath+'/panel/vhost/rewrite';
        urlrewriteFile = urlrewritePath+'/'+self.siteName+'.conf';
        if not os.path.exists(urlrewritePath): os.makedirs(urlrewritePath);
        open(urlrewriteFile,'w+').close();
        return True;
    
     
    #添加站点
    def AddSite(self,get):
        import json,files
        siteMenu = json.loads(get.webname)
        self.siteName     = self.ToPunycode(siteMenu['domain'].split(':')[0]);
        self.sitePath     = self.ToPunycodePath(self.GetPath(get.path.replace(' ','')));
        self.sitePort     = get.port.replace(' ','');
        
        if self.sitePort == "": get.port = "80";
        if not public.checkPort(self.sitePort): return public.returnMsg(False,'SITE_ADD_ERR_PORT');
        
        if hasattr(get,'version'):
            self.phpVersion   = get.version.replace(' ','');
        else:
            self.phpVersion   = '54';
        
        
        domain = None
        #if siteMenu['count']:
        #    domain            = get.domain.replace(' ','')
        #表单验证
        if not files.files().CheckDir(self.sitePath): return public.returnMsg(False,'PATH_ERROR');
        if len(self.phpVersion) < 2: return public.returnMsg(False,'SITE_ADD_ERR_PHPEMPTY');
        reg = "^([\w\-\*]{1,100}\.){1,4}([\w\-]{1,24}|[\w\-]{1,24}\.[\w\-]{1,24})$";
        if not re.match(reg, self.siteName): return public.returnMsg(False,'SITE_ADD_ERR_DOMAIN');
        if self.siteName.find('*') != -1: return public.returnMsg(False,'SITE_ADD_ERR_DOMAIN_TOW');
        
        if not domain: domain = self.siteName;
    
        
        #是否重复
        sql = public.M('sites');
        
        if sql.where("name=?",(self.siteName,)).count(): return public.returnMsg(False,'SITE_ADD_ERR_EXISTS');
        if public.M('domain').where("name=?",(self.siteName,)).count(): return public.returnMsg(False,'SITE_ADD_ERR_DOMAIN_EXISTS');
        
        #创建根目录
        if not os.path.exists(self.sitePath): 
            os.makedirs(self.sitePath)
            public.ExecShell('chmod -R 755 ' + self.sitePath);
            public.ExecShell('chown -R www:www ' + self.sitePath);
        
        #创建basedir
        userIni = self.sitePath+'/.user.ini';
        if not os.path.exists(userIni):
            public.writeFile(userIni, 'open_basedir='+self.sitePath+'/:/tmp/:/proc/');
            public.ExecShell('chmod 644 ' + userIni);
            public.ExecShell('chown root:root ' + userIni);
            public.ExecShell('chattr +i '+userIni);
        
        #创建默认文档
        index = self.sitePath+'/index.html'
        if not os.path.exists(index):
            public.writeFile(index, public.readFile('data/defaultDoc.html'))
        
        #创建自定义404页
        doc404 = self.sitePath+'/404.html'
        if not os.path.exists(doc404):
            public.writeFile(doc404, public.readFile('data/404.html'));
        
        #写入配置
        result = self.nginxAdd()
        result = self.apacheAdd()
        
        #检查处理结果
        if not result: return public.returnMsg(False,'SITE_ADD_ERR_WRITE');
        
        ps = get.ps
        #添加放行端口
        if self.sitePort != '80':
            import firewalls
            get.port = self.sitePort
            get.ps = self.siteName;
            firewalls.firewalls().AddAcceptPort(get);
        
        #写入数据库
        get.pid = sql.table('sites').add('name,path,status,ps,addtime',(self.siteName,self.sitePath,'1',ps,public.getDate()))
        
        #添加更多域名
        for domain in siteMenu['domainlist']:
            get.domain = domain
            get.webname = self.siteName
            get.id = str(get.pid)
            self.AddDomain(get)
        
        sql.table('domain').add('pid,name,port,addtime',(get.pid,self.siteName,self.sitePort,public.getDate()))
        
        data = {}
        data['siteStatus'] = True
            
        #添加FTP
        data['ftpStatus'] = False
        if get.ftp == 'true':
            import ftp
            get.ps = self.siteName
            result = ftp.ftp().AddUser(get)
            if result['status']: 
                data['ftpStatus'] = True
                data['ftpUser'] = get.ftp_username
                data['ftpPass'] = get.ftp_password
        
        #添加数据库
        data['databaseStatus'] = False
        if get.sql == 'true':
            import database
            get.name = get.datauser
            get.password = get.datapassword
            get.address = '127.0.0.1'
            get.ps = self.siteName
            result = database.database().AddDatabase(get)
            if result['status']: 
                data['databaseStatus'] = True
                data['databaseUser'] = get.datauser
                data['databasePass'] = get.datapassword
        public.serviceReload()
        public.WriteLog('TYPE_SITE','SITE_ADD_SUCCESS',(self.siteName,))
        return data
    
    #删除站点
    def DeleteSite(self,get):
        id = get.id;
        siteName = get.webname;
        get.siteName = siteName
        self.CloseTomcat(get);
        
        #删除配置文件
        confPath = self.setupPath+'/panel/vhost/nginx/'+siteName+'.conf'
        if os.path.exists(confPath): os.remove(confPath)
        
        confPath = self.setupPath+'/panel/vhost/apache/' + siteName + '.conf';
        if os.path.exists(confPath): os.remove(confPath)
        
        #删除伪静态文件
        filename = confPath+'/rewrite/'+siteName+'.conf'
        if os.path.exists(filename): 
            os.remove(filename)
            public.ExecShell("rm -f " + confPath + '/rewrite/' + siteName + "_*")
        
        #删除日志文件
        filename = web.ctx.session.logsPath+'/'+siteName+'*'
        public.ExecShell("rm -f " + filename)
        
        
        #删除证书
        #crtPath = '/etc/letsencrypt/live/'+siteName
        #if os.path.exists(crtPath):
        #    import shutil
        #    shutil.rmtree(crtPath)
        
        #删除日志
        public.ExecShell("rm -f " + web.ctx.session.logsPath + '/' + siteName + "-*")
        
        #删除备份
        public.ExecShell("rm -f "+web.ctx.session.config['backup_path']+'/site/'+siteName+'_*')
        
        #删除根目录
        if hasattr(get,'path'):
            import files
            get.path = public.M('sites').where("id=?",(id,)).getField('path');
            files.files().DeleteDir(get)
        
        #重载配置
        public.serviceReload();
        
        #从数据库删除
        public.M('sites').where("id=?",(id,)).delete();
        public.M('binding').where("pid=?",(id,)).delete();
        public.M('domain').where("pid=?",(id,)).delete();
        public.WriteLog('TYPE_SITE', "SITE_DEL_SUCCESS",(siteName,));
        
        #是否删除关联数据库
        if hasattr(get,'database'):
            find = public.M('databases').where("pid=?",(id,)).field('id,name').find()
            if find:
                import database
                get.name = find['name']
                get.id = find['id']
                database.database().DeleteDatabase(get)
        
        #是否删除关联FTP
        if hasattr(get,'ftp'):
            find = public.M('ftps').where("pid=?",(id,)).field('id,name').find()
            if find:
                import ftp
                get.username = find['name']
                get.id = find['id']
                ftp.ftp().DeleteUser(get)
            
        return public.returnMsg(True,'SITE_DEL_SUCCESS')
    
    #域名编码转换
    def ToPunycode(self,domain):
        import re;
        domain = domain.encode('utf8');
        tmp = domain.split('.');
        newdomain = '';
        for dkey in tmp:
                #匹配非ascii字符
                match = re.search(u"[\x80-\xff]+",dkey);
                if not match:
                    newdomain += dkey + '.';
                else:
                    newdomain += 'xn--' + dkey.decode('utf-8').encode('punycode') + '.'
        return newdomain[0:-1];
    
    #中文路径处理
    def ToPunycodePath(self,path):
        path = path.encode('utf-8');
        import re;
        match = re.search(u"[\x80-\xff]+",path);
        if not match: return path;
        npath = '';
        for ph in path.split('/'):
            npath += '/' + self.ToPunycode(ph);
        return npath.replace('//','/')
        
    #添加域名
    def AddDomain(self,get):
        if len(get.domain) < 3: return public.returnMsg(False,'SITE_ADD_DOMAIN_ERR_EMPTY');
        domains = get.domain.split(',')
        for domain in domains:
            if domain == "": continue;
            domain = domain.split(':')
            get.domain = self.ToPunycode(domain[0])
            get.port = '80'
            
            reg = "^([\w\-\*]{1,100}\.){1,4}([\w\-]{1,24}|[\w\-]{1,24}\.[\w\-]{1,24})$";
            if not re.match(reg, get.domain): return public.returnMsg(False,'SITE_ADD_DOMAIN_ERR_FORMAT');
            
            if len(domain) == 2: get.port = domain[1];
            if get.port == "": get.port = "80";
            
            if not public.checkPort(get.port): return public.returnMsg(False,'SITE_ADD_DOMAIN_ERR_POER');
            #检查域名是否存在
            sql = public.M('domain');
            if sql.where("name=? AND (port=? OR pid=?)",(get.domain,get.port,get.id)).count() > 0: return public.returnMsg(False,'SITE_ADD_DOMAIN_ERR_EXISTS');
            
            #写配置文件
            self.NginxDomain(get)
            try:
                self.ApacheDomain(get)
            except:
                pass;
            
            #检查配置文件
            isError = public.checkWebConfig()
            
            if isError != True:
                try:
                    import shutil
                    shutil.copyfile('/tmp/backup.conf',file);
                    return public.returnMsg(False,'CONF_ERROR: <br><a style="color:red;">'+isError.replace("\n",'<br>')+'</a>');
                except:
                    pass
            
            #添加放行端口
            if get.port != '80':
                import firewalls
                get.ps = get.domain;
                firewalls.firewalls().AddAcceptPort(get);
            
            public.serviceReload();
            public.WriteLog('TYPE_SITE', 'DOMAIN_ADD_SUCCESS',(get.webname,get.domain));
            sql.table('domain').add('pid,name,port,addtime',(get.id,get.domain,get.port,public.getDate()));
        return public.returnMsg(True,'SITE_ADD_DOMAIN');
    
    #Nginx写域名配置
    def NginxDomain(self,get):
        file = self.setupPath + '/panel/vhost/nginx/'+get.webname+'.conf';
        conf = public.readFile(file);
        if not conf: return;
        
        #添加域名
        rep = "server_name\s*(.*);";
        tmp = re.search(rep,conf).group()
        domains = tmp.split(' ')
        if not public.inArray(domains,get.domain):
            newServerName = tmp.replace(';',' ' + get.domain + ';')
            conf = conf.replace(tmp,newServerName)
        
        #添加端口
        rep = "listen\s+([0-9]+)\s*[default_server]*\s*;";
        tmp = re.findall(rep,conf);
        if not public.inArray(tmp,get.port):
            listen = re.search(rep,conf).group()
            conf = conf.replace(listen,listen + "\n\tlisten "+get.port+';')
        #保存配置文件
        import shutil
        shutil.copyfile(file, '/tmp/backup.conf')
        public.writeFile(file,conf)
        return True
    
    #Apache写域名配置
    def ApacheDomain(self,get):
        file = self.setupPath + '/panel/vhost/apache/'+get.webname+'.conf';
        conf = public.readFile(file);
        if not conf: return;
        
        port = get.port;
        siteName = get.webname;
        newDomain = get.domain
        find = public.M('sites').where("id=?",(get.id,)).field('id,name,path').find();
        sitePath = find['path'];
        siteIndex = 'index.php index.html index.htm default.php default.html default.htm'
            
        #添加域名
        if conf.find('<VirtualHost *:'+port+'>') != -1:
            repV = "<VirtualHost\s+\*\:"+port+">(.|\n)*</VirtualHost>";
            domainV = re.search(repV,conf).group()
            rep = "ServerAlias\s*(.*)\n";
            tmp = re.search(rep,domainV).group(0)
            domains = tmp[1].split(' ')
            if not public.inArray(domains,newDomain):
                rs = tmp.replace("\n","")
                newServerName = rs+' '+newDomain+"\n";
                myconf = domainV.replace(tmp,newServerName);
                conf = re.sub(repV, myconf, conf);
        else:
            try:
                httpdVersion = public.readFile(self.setupPath+'/apache/version.pl').strip();
            except:
                httpdVersion = "";
            if httpdVersion == '2.2':
                vName = "NameVirtualHost  *:"+port+"\n";
                phpConfig = "";
                apaOpt = "Order allow,deny\n\t\tAllow from all";
            else:
                vName = "";
                rep = "php-cgi-([0-9]{2,3})\.sock";
                version = re.search(rep,conf).groups()[0]
                if len(version) < 2: return public.returnMsg(False,'PHP_GET_ERR')
                phpConfig ='''
    #PHP
    <FilesMatch \\.php$>
            SetHandler "proxy:unix:/tmp/php-cgi-%s.sock|fcgi://localhost"
    </FilesMatch>
    ''' % (version,);
                apaOpt = 'Require all granted';
            
            newconf='''<VirtualHost *:%s>
    ServerAdmin webmaster@example.com
    DocumentRoot "%s"
    ServerName %s.%s
    ServerAlias %s
    errorDocument 404 /404.html
    ErrorLog "%s-error_log"
    CustomLog "%s-access_log" combined
    %s
    #PATH
    <Directory "%s">
        SetOutputFilter DEFLATE
        Options FollowSymLinks
        AllowOverride All
        %s
        DirectoryIndex %s
    </Directory>
</VirtualHost>''' % (port,sitePath,siteName,port,newDomain,web.ctx.session.logsPath+'/'+siteName,web.ctx.session.logsPath+'/'+siteName,phpConfig,sitePath,apaOpt,siteIndex)
            conf += "\n\n"+newconf;
        
        #添加端口
        if port != '80' and port != '888': self.apacheAddPort(port)
        
        #保存配置文件
        import shutil
        shutil.copyfile(file, '/tmp/backup.conf')
        public.writeFile(file,conf)
        return True
    
    #删除域名
    def DelDomain(self,get):
        sql = public.M('domain');
        id=get['id'];
        port = get.port;
        find = sql.where("pid=? AND name=?",(get.id,get.domain)).field('id,name').find();
        domain_count = sql.table('domain').where("pid=?",(id,)).count();
        if domain_count == 1: return public.returnMsg(False,'SITE_DEL_DOMAIN_ERR_ONLY');
        
        #nginx
        file = self.setupPath+'/panel/vhost/nginx/'+get['webname']+'.conf';
        conf = public.readFile(file);
        if conf:
            #删除域名
            rep = "server_name\s+(.+);";
            tmp = re.search(rep,conf).group()
            newServerName = tmp.replace(' '+get['domain']+';',';');
            newServerName = newServerName.replace(' '+get['domain']+' ',' ');
            conf = conf.replace(tmp,newServerName);
            
            #删除端口
            rep = "listen\s+([0-9]+);";
            tmp = re.findall(rep,conf);
            port_count = sql.table('domain').where('pid=? AND port=?',(get.id,get.port)).count()
            if public.inArray(tmp,port) == True and  port_count < 2:
                rep = "\n*\s+listen\s+"+port+";";
                conf = re.sub(rep,'',conf);
            #保存配置
            public.writeFile(file,conf)
        
        #apache
        file = self.setupPath+'/panel/vhost/apache/'+get['webname']+'.conf';
        conf = public.readFile(file);
        if conf:
            #删除域名
            try:
                rep = "\n*<VirtualHost \*\:" + port + ">(.|\n)*</VirtualHost>";
                tmp = re.search(rep, conf).group()
                
                rep1 = "ServerAlias\s+(.+)\n";
                tmp1 = re.findall(rep1,tmp);
                tmp2 = tmp1[0].split(' ')
                if len(tmp2) < 2:
                    conf = re.sub(rep,'',conf);
                    rep = "NameVirtualHost.+\:" + port + "\n";
                    conf = re.sub(rep,'',conf);
                else:
                    newServerName = tmp.replace(' '+get['domain']+"\n","\n");
                    newServerName = newServerName.replace(' '+get['domain']+' ',' ');
                    conf = conf.replace(tmp,newServerName);
            
                #保存配置
                public.writeFile(file,conf)
            except:
                pass;
        
        sql.table('domain').where("id=?",(find['id'],)).delete();
        public.WriteLog('TYPE_SITE', 'DOMAIN_DEL_SUCCESS',(get.webname,get.domain));
        public.serviceReload();
        return public.returnMsg(True,'DEL_SUCCESS');
    
    #检查域名是否解析
    def CheckDomainPing(self,get):
        try:
            epass = public.GetRandomString(32);
            spath = get.path + '/.well-known/pki-validation';
            if not os.path.exists(spath): os.system("mkdir -p '" + spath + "'");
            public.writeFile(spath + '/fileauth.txt',epass);
            result = public.httpGet('http://' + get.domain + '/.well-known/pki-validation/fileauth.txt');
            if result == epass: return True
            return False
        except:
            return False
    
    #保存第三方证书
    def SetSSL(self,get):
        type = get.type;
        siteName = get.siteName;
        path =   '/etc/letsencrypt/live/'+ siteName;
        if not os.path.exists(path):
            public.ExecShell('mkdir -p ' + path)
        
        csrpath = path+"/fullchain.pem";                    #生成证书路径  
        keypath = path+"/privkey.pem";                      #密钥文件路径  
         
        if(get.key.find('KEY') == -1): return public.returnMsg(False, 'SITE_SSL_ERR_PRIVATE');
        if(get.csr.find('CERTIFICATE') == -1): return public.returnMsg(False, 'SITE_SSL_ERR_CERT');
        
        public.ExecShell('\\cp -a '+keypath+' /tmp/backup1.conf');
        public.writeFile(keypath,get.key);
        
        public.ExecShell('\\cp -a '+csrpath+' /tmp/backup2.conf');
        public.writeFile(csrpath,get.csr);
        
        isError = public.checkWebConfig();
    
        if(isError != True):
            public.ExecShell('\\cp -a /tmp/backup1.conf ' + keypath);
            public.ExecShell('\\cp -a /tmp/backup2.conf ' + csrpath);
            return public.returnMsg(False,'ERROR: <br><a style="color:red;">'+isError.replace("\n",'<br>')+'</a>');
        #写入配置文件
        self.SetSSLConf(get);
        public.serviceReload();
        
        #清理旧的证书链
        if os.path.exists(path+'/README'):
            public.ExecShell('rm -rf ' + path);
            public.ExecShell('rm -rf ' + path + '-00*');
            public.ExecShell('rm -rf /etc/letsencrypt/archive/' + get.siteName);
            public.ExecShell('rm -rf /etc/letsencrypt/archive/' + get.siteName + '-00*');
            public.ExecShell('rm -f /etc/letsencrypt/renewal/'+ get.siteName + '.conf');
            public.ExecShell('rm -f /etc/letsencrypt/renewal/'+ get.siteName + '-00*.conf');
            public.ExecShell('rm -f ' + path + '/README');
            
        if os.path.exists(path + '/partnerOrderId'): os.system('rm -f ' + path + '/partnerOrderId');
        public.WriteLog('TYPE_SITE','SITE_SSL_SAVE_SUCCESS');
        return public.returnMsg(True,'SITE_SSL_SUCCESS');
        
    #获取运行目录
    def GetRunPath(self,get):
        if hasattr(get,'siteName'):
            get.id = public.M('sites').where('name=?',(get.siteName,)).getField('id');
        else:
            get.id = public.M('sites').where('path=?',(get.path,)).getField('id');
        if not get.id: return False;
        import panelSite
        result = self.GetSiteRunPath(get);
        return result['runPath'];
    
    #创建Let's Encrypt免费证书
    def CreateLet(self,get):
        
        #检查是否设置301
        serverTypes = ['nginx','apache'];
        for stype in serverTypes:
            file = self.setupPath + '/panel/vhost/'+stype+'/'+get.siteName+'.conf';
            if os.path.exists(file):
                siteConf = public.readFile(file);
                if siteConf.find('301-START') != -1: return public.returnMsg(False,'SITE_SSL_ERR_301');
        
        #定义证书存放目录       
        path =   '/etc/letsencrypt/live/'+ get.siteName;
        csrpath = path+"/fullchain.pem";                    #生成证书路径
        keypath = path+"/privkey.pem";                      #密钥文件路径
                
        #准备基础信息
        actionstr = get.updateOf
        siteInfo = public.M('sites').where('name=?',(get.siteName,)).field('id,name,path').find();
        runPath = self.GetRunPath(get);
        if runPath != False and runPath != '/': siteInfo['path'] +=  runPath;
        get.path = siteInfo['path'];
        #domains = public.M('domain').where("pid=?",(siteInfo['id'],)).field('name').select()
        import json
        domains = json.loads(get.domains)
        execStr = 'echo ' + actionstr + '|' + self.setupPath + "/panel/certbot-auto certonly -n --email 287962566@qq.com --agree-tos --webroot -w "+siteInfo['path'];
        
        #确定主域名顺序
        domainsTmp = []
        if get.siteName in domains: domainsTmp.append(get.siteName);
        for domainTmp in domains:
            if domainTmp == get.siteName: continue;
            domainsTmp.append(domainTmp);
        domains = domainsTmp;
        
        #构造参数
        domainCount = 0
        errorDomain = "";
        for domain in domains:
            if public.checkIp(domain): continue;
            if domain.find('*') != -1: continue;
            get.domain = domain;
            if not self.CheckDomainPing(get): errorDomain += '<li>' + domain + '</li>';
            execStr += ' -d ' + domain
            domainCount += 1
        
        if errorDomain: return public.returnMsg(False,'SITE_SSL_ERR_DNS',('<span style="color:red;"><br>'+errorDomain+'</span>',));
        #获取域名数据
        if domainCount == 0: return public.returnMsg(False,'SITE_SSL_ERR_EMPTY')
        
        #检查是否自定义证书
        partnerOrderId =   path + '/partnerOrderId';
        if os.path.exists(partnerOrderId): public.ExecShell('rm -rf ' + partnerOrderId);
        self.CloseSSLConf(get);
        
        public.ExecShell('rm -rf ' + path)
        public.ExecShell('rm -rf ' + path + '-00*')
        public.ExecShell('rm -rf /etc/letsencrypt/archive/' + get.siteName)
        public.ExecShell('rm -rf /etc/letsencrypt/archive/' + get.siteName + '-00*')
        public.ExecShell('rm -f /etc/letsencrypt/renewal/'+ get.siteName + '.conf')
        public.ExecShell('rm -f /etc/letsencrypt/renewal/'+ get.siteName + '-00*.conf')
        public.ExecShell('rm -f ' + path + '/README');
        if os.path.exists(path + '/partnerOrderId'): os.system('rm -f ' + path + '/partnerOrderId');
        
        result = public.ExecShell(execStr);
        
        #判断是否获取成功
        if not os.path.exists(csrpath): 
             data = {}
             data['out'] = self.GetFormatSSLResult(result[0])           #返回错误信息
             data['err'] = result;
             data['status'] = False
             data['msg'] = public.getMsg('SITE_SSL_ERR_ACCESS');
             if result[1].find('Certificate not yet due for renewal') != -1: data['msg'] = public.getMsg('SITE_SSL_ERR_RE');
             if result[0].find('Too many invalid authorizations recently') != -1: data['msg'] = public.getMsg('SITE_SSL_ERR_AU');
             return data
        
        public.ExecShell('echo "let" > ' + path + '/README');
        if(actionstr == '2'): return public.returnMsg(True,'SITE_SSL_UPDATE_SUCCESS');
        
        #写入配置文件
        result =  self.SetSSLConf(get);
        result['csr'] = public.readFile(csrpath);
        result['key'] = public.readFile(keypath);
        public.serviceReload();
        return result;
        
    
    def GetFormatSSLResult(self,result):
        try:
            import re
            rep = "\s*Domain:.+\n\s+Type:.+\n\s+Detail:.+"
            tmps = re.findall(rep,result);
        
            statusList = [];
            for tmp in tmps:
                arr = tmp.strip().split('\n')
                status={}
                for ar in arr:
                    tmp1 = ar.strip().split(':');
                    status[tmp1[0].strip()] = tmp1[1].strip();
                    if len(tmp1) > 2:
                        status[tmp1[0].strip()] = tmp1[1].strip() + ':' + tmp1[2];
                statusList.append(status);        
            return statusList;
        except:
            return None;
        
    #添加SSL配置
    def SetSSLConf(self,get):
        import shutil
        siteName = get.siteName
        
        #Nginx配置
        file = self.setupPath + '/panel/vhost/nginx/'+siteName+'.conf';
        conf = public.readFile(file);
        
        #是否为子目录设置SSL
        #if hasattr(get,'binding'):
        #    allconf = conf;
        #    conf = re.search("#BINDING-"+get.binding+"-START(.|\n)*#BINDING-"+get.binding+"-END",conf).group();
            
        if conf:
            if conf.find('ssl_certificate') == -1: 
                sslStr = """#error_page 404/404.html;
    ssl_certificate    /etc/letsencrypt/live/%s/fullchain.pem;
    ssl_certificate_key    /etc/letsencrypt/live/%s/privkey.pem;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4:!DH:!DHE;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    error_page 497  https://$host$request_uri;
""" % (siteName,siteName);
                if(conf.find('ssl_certificate') != -1):
                    return public.returnMsg(True,'SITE_SSL_OPEN_SUCCESS');
                
            
                conf = conf.replace('#error_page 404/404.html;',sslStr);                
                #添加端口
                rep = "listen\s+([0-9]+)\s*[default_server]*;";
                tmp = re.findall(rep,conf);
                if not public.inArray(tmp,'443'):
                    listen = re.search(rep,conf).group()
                    versionStr = public.readFile('/www/server/nginx/version.pl');
                    http2 = ''
                    if versionStr:
                        if versionStr.find('1.8.1') == -1: http2 = ' http2';
                    conf = conf.replace(listen,listen + "\n\tlisten 443 ssl"+http2+";")
                if web.ctx.session.webserver == 'nginx': shutil.copyfile(file, '/tmp/backup.conf')
                public.writeFile(file,conf)
            
        #Apache配置
        file = self.setupPath + '/panel/vhost/apache/'+siteName+'.conf';
        conf = public.readFile(file);
        if conf:
            if conf.find('SSLCertificateFile') == -1:
                find = public.M('sites').where("name=?",(siteName,)).field('id,path').find();
                tmp = public.M('domain').where('pid=?',(find['id'],)).field('name').select()
                domains = ''
                for key in tmp:
                    domains += key['name'] + ' '
                path = (find['path'] + '/' + self.GetRunPath(get)).replace('//','/');
                index = 'index.php index.html index.htm default.php default.html default.htm'
                
                try:
                    httpdVersion = public.readFile(self.setupPath+'/apache/version.pl').strip();
                except:
                    httpdVersion = "";
                if httpdVersion == '2.2':
                    vName = "";
                    phpConfig = "";
                    apaOpt = "Order allow,deny\n\t\tAllow from all";
                else:
                    vName = "";
                    rep = "php-cgi-([0-9]{2,3})\.sock";
                    version = re.search(rep,conf).groups()[0];
                    if len(version) < 2: return public.returnMsg(False,'PHP_GET_ERR');
                    phpConfig ='''
    #PHP
    <FilesMatch \\.php$>
            SetHandler "proxy:unix:/tmp/php-cgi-%s.sock|fcgi://localhost"
    </FilesMatch>
    ''' % (version,);
                    apaOpt = 'Require all granted';
                
                try:
                    sslStr = '''%s<VirtualHost *:443>
    ServerAdmin webmasterexample.com
    DocumentRoot "%s"
    ServerName SSL.%s
    ServerAlias %s
    errorDocument 404 /404.html
    ErrorLog "%s-error_log"
    CustomLog "%s-access_log" combined
    
    #SSL
    SSLEngine On
    SSLCertificateFile /etc/letsencrypt/live/%s/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/%s/privkey.pem
    SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
    SSLProtocol All -SSLv2 -SSLv3
    SSLHonorCipherOrder On
    %s
    #PATH
    <Directory "%s">
        SetOutputFilter DEFLATE
        Options FollowSymLinks
        AllowOverride All
        %s
        DirectoryIndex %s
    </Directory>
</VirtualHost>''' % (vName,path,siteName,domains,web.ctx.session.logsPath + '/' + siteName,web.ctx.session.logsPath + '/' + siteName,siteName,siteName,phpConfig,path,apaOpt,index)
                    
                    conf = conf+"\n"+sslStr;
                    self.apacheAddPort('443');
                    if web.ctx.session.webserver == 'apache': shutil.copyfile(file, '/tmp/backup.conf')
                    public.writeFile(file,conf)
                except Exception,ex:
                    return str(ex);
                    pass
        isError = public.checkWebConfig();
        if(isError != True):
            shutil.copyfile('/tmp/backup.conf',file)
            return public.returnMsg(False,'ERROR: <br><a style="color:red;">'+isError.replace("\n",'<br>')+'</a>');
        
        
        sql = public.M('firewall');
        import firewalls
        get.port = '443'
        get.ps = 'HTTPS'
        firewalls.firewalls().AddAcceptPort(get)
        public.serviceReload();
        public.WriteLog('TYPE_SITE', 'SITE_SSL_OPEN_SUCCESS',(siteName,));
        return public.returnMsg(True,'SITE_SSL_OPEN_SUCCESS');
    
    #HttpToHttps
    def HttpToHttps(self,get):
        siteName = get.siteName;
        #Nginx配置
        file = self.setupPath + '/panel/vhost/nginx/'+siteName+'.conf';
        conf = public.readFile(file);
        if conf:
            if conf.find('ssl_certificate') == -1: return public.returnMsg(False,'当前未开启SSL');
            to = """#error_page 404/404.html;
    #HTTP_TO_HTTPS_START
    if ($server_port !~ 443){
        rewrite ^(/.*)$ https://$host$1 permanent;
    }
    #HTTP_TO_HTTPS_END"""
            conf = conf.replace('#error_page 404/404.html;',to);
            public.writeFile(file,conf);
        
        file = self.setupPath + '/panel/vhost/apache/'+siteName+'.conf';
        conf = public.readFile(file);
        if conf:
            httpTohttos = '''combined
    #HTTP_TO_HTTPS_START
    <IfModule mod_rewrite.c>
        RewriteEngine on
        RewriteCond %{SERVER_PORT} !^443$
        RewriteRule (.*) https://%{SERVER_NAME}$1 [L,R=301]
    </IfModule>
    #HTTP_TO_HTTPS_END'''
            conf = re.sub('combined',httpTohttos,conf,1);
            public.writeFile(file,conf);
        public.serviceReload();
        return public.returnMsg(True,'SET_SUCCESS');
    
    #CloseToHttps
    def CloseToHttps(self,get):
        siteName = get.siteName;
        file = self.setupPath + '/panel/vhost/nginx/'+siteName+'.conf';
        conf = public.readFile(file);
        if conf:
            rep = "\n\s*#HTTP_TO_HTTPS_START(.|\n){1,300}#HTTP_TO_HTTPS_END";
            conf = re.sub(rep,'',conf);
            rep = "\s+if.+server_port.+\n.+\n\s+\s*}";
            conf = re.sub(rep,'',conf);
            public.writeFile(file,conf);
        
        file = self.setupPath + '/panel/vhost/apache/'+siteName+'.conf';
        conf = public.readFile(file);
        if conf:
            rep = "\n\s*#HTTP_TO_HTTPS_START(.|\n){1,300}#HTTP_TO_HTTPS_END";
            conf = re.sub(rep,'',conf);
            public.writeFile(file,conf);
        public.serviceReload();
        return public.returnMsg(True,'SET_SUCCESS');
    
    #是否跳转到https
    def IsToHttps(self,siteName):
        file = self.setupPath + '/panel/vhost/nginx/'+siteName+'.conf';
        conf = public.readFile(file);
        if conf:
            if conf.find('HTTP_TO_HTTPS_START') != -1: return True;
            if conf.find('$server_port !~ 443') != -1: return True;
        return False;
        
    #清理SSL配置
    def CloseSSLConf(self,get):
        siteName = get.siteName
        
        file = self.setupPath + '/panel/vhost/nginx/'+siteName+'.conf';
        conf = public.readFile(file);
        if conf:
            rep = "\n\s*#HTTP_TO_HTTPS_START(.|\n){1,300}#HTTP_TO_HTTPS_END";
            conf = re.sub(rep,'',conf);
            rep = "\s+ssl_certificate\s+.+;\s+ssl_certificate_key\s+.+;";
            conf = re.sub(rep,'',conf);
            rep = "\s+ssl_protocols\s+.+;\n";
            conf = re.sub(rep,'',conf);
            rep = "\s+ssl_ciphers\s+.+;\n";
            conf = re.sub(rep,'',conf);
            rep = "\s+ssl_prefer_server_ciphers\s+.+;\n";
            conf = re.sub(rep,'',conf);
            rep = "\s+ssl_session_cache\s+.+;\n";
            conf = re.sub(rep,'',conf);
            rep = "\s+ssl_session_timeout\s+.+;\n";
            conf = re.sub(rep,'',conf);
            rep = "\s+ssl_ecdh_curve\s+.+;\n";
            conf = re.sub(rep,'',conf);
            rep = "\s+ssl_session_tickets\s+.+;\n";
            conf = re.sub(rep,'',conf);
            rep = "\s+ssl_stapling\s+.+;\n";
            conf = re.sub(rep,'',conf);
            rep = "\s+ssl_stapling_verify\s+.+;\n";
            conf = re.sub(rep,'',conf);
            rep = "\s+add_header\s+.+;\n";
            conf = re.sub(rep,'',conf);
            rep = "\s+add_header\s+.+;\n";
            conf = re.sub(rep,'',conf);
            rep = "\s+ssl\s+on;";
            conf = re.sub(rep,'',conf);
            rep = "\s+error_page\s497.+;";
            conf = re.sub(rep,'',conf);
            rep = "\s+if.+server_port.+\n.+\n\s+\s*}";
            conf = re.sub(rep,'',conf);
            rep = "\s+listen\s+443.*;";
            conf = re.sub(rep,'',conf);
            public.writeFile(file,conf)
    
        file = self.setupPath + '/panel/vhost/apache/'+siteName+'.conf';
        conf = public.readFile(file);
        if conf:
            rep = "\n<VirtualHost \*\:443>(.|\n)*<\/VirtualHost>";
            conf = re.sub(rep,'',conf);
            rep = "\n\s*#HTTP_TO_HTTPS_START(.|\n){1,250}#HTTP_TO_HTTPS_END";
            conf = re.sub(rep,'',conf);
            rep = "NameVirtualHost  *:443\n";
            conf = conf.replace(rep,'');
            public.writeFile(file,conf)
        
        partnerOrderId =   '/etc/letsencrypt/live/'+ siteName + '/partnerOrderId';
        if os.path.exists(partnerOrderId): public.ExecShell('rm -f ' + partnerOrderId);
        public.WriteLog('TYPE_SITE', 'SITE_SSL_CLOSE_SUCCESS',(siteName,));
        public.serviceReload();
        return public.returnMsg(True,'SITE_SSL_CLOSE_SUCCESS');
    
    
    #取SSL状态
    def GetSSL(self,get):
        siteName = get.siteName
        path =   '/etc/letsencrypt/live/'+ siteName;
        type = 0;
        if os.path.exists(path+'/README'):  type = 1;
        if os.path.exists(path+'/partnerOrderId'):  type = 2;
        csrpath = path+"/fullchain.pem";                    #生成证书路径  
        keypath = path+"/privkey.pem";                      #密钥文件路径
        key = public.readFile(keypath);
        csr = public.readFile(csrpath);
        file = self.setupPath + '/panel/vhost/' + web.ctx.session.webserver + '/'+siteName+'.conf';
        conf = public.readFile(file);
        keyText = 'SSLCertificateFile'
        if web.ctx.session.webserver == 'nginx': keyText = 'ssl_certificate';
        status = True
        if(conf.find(keyText) == -1): 
            status = False
            type = -1
        
        toHttps = self.IsToHttps(siteName);
        id = public.M('sites').where("name=?",(siteName,)).getField('id');
        domains = public.M('domain').where("pid=?",(id,)).field('name').select();
        return {'status':status,'domain':domains,'key':key,'csr':csr,'type':type,'httpTohttps':toHttps}
    
    
    #启动站点
    def SiteStart(self,get):
        id = get.id
        Path = self.setupPath + '/stop';
        sitePath = public.M('sites').where("id=?",(id,)).getField('path');
        
        #nginx
        file = self.setupPath + '/panel/vhost/nginx/'+get.name+'.conf';
        conf = public.readFile(file);
        if conf:
            conf = conf.replace(Path, sitePath);
            public.writeFile(file,conf)
        #apaceh
        file = self.setupPath + '/panel/vhost/apache/'+get.name+'.conf';
        conf = public.readFile(file);
        if conf:
            conf = conf.replace(Path, sitePath);
            public.writeFile(file,conf)
        
        public.M('sites').where("id=?",(id,)).setField('status','1');
        public.serviceReload();
        public.WriteLog('TYPE_SITE','SITE_START_SUCCESS',(get.name,))
        return public.returnMsg(True,'SITE_START_SUCCESS')
    
    
    #停止站点
    def SiteStop(self,get):
        path = self.setupPath + '/stop';
        if not os.path.exists(path):
            os.makedirs(path)
            public.downloadFile('http://download.bt.cn/stop.html',path + '/index.html');
        
        
        id = get.id
        sitePath = public.M('sites').where("id=?",(id,)).getField('path');
        
        #nginx
        file = self.setupPath + '/panel/vhost/nginx/'+get.name+'.conf';
        conf = public.readFile(file);
        if conf:
            conf = conf.replace(sitePath,path);
            public.writeFile(file,conf)
        #apache
        file = self.setupPath + '/panel/vhost/apache/'+get.name+'.conf';
        conf = public.readFile(file);
        if conf:
            conf = conf.replace(sitePath,path);
            public.writeFile(file,conf)
        
        public.M('sites').where("id=?",(id,)).setField('status','0');
        public.serviceReload();
        public.WriteLog('TYPE_SITE','SITE_STOP_SUCCESS',(get.name,))
        return public.returnMsg(True,'SITE_STOP_SUCCESS')

    
    #取流量限制值
    def GetLimitNet(self,get):
        id = get.id
        
        #取回配置文件
        siteName = public.M('sites').where("id=?",(id,)).getField('name');
        filename = self.setupPath + '/panel/vhost/nginx/'+siteName+'.conf';
        
        #站点总并发
        data = {}
        conf = public.readFile(filename);
        try:
            rep = "\s+limit_conn\s+perserver\s+([0-9]+);";
            tmp = re.search(rep, conf).groups()
            data['perserver'] = int(tmp[0]);
            
            #IP并发限制
            rep = "\s+limit_conn\s+perip\s+([0-9]+);";
            tmp = re.search(rep, conf).groups()
            data['perip'] = int(tmp[0]);
            
            #请求并发限制
            rep = "\s+limit_rate\s+([0-9]+)\w+;";
            tmp = re.search(rep, conf).groups()
            data['limit_rate'] = int(tmp[0]);
        except:
            data['perserver'] = 0
            data['perip'] = 0
            data['limit_rate'] = 0
        
        return data;
    
    
    #设置流量限制
    def SetLimitNet(self,get):
        if(web.ctx.session.webserver != 'nginx'): return public.returnMsg(False, 'SITE_NETLIMIT_ERR');
        
        id = get.id;
        perserver = 'limit_conn perserver ' + get.perserver + ';';
        perip = 'limit_conn perip ' + get.perip + ';';
        limit_rate = 'limit_rate ' + get.limit_rate + 'k;';
        
        #取回配置文件
        siteName = public.M('sites').where("id=?",(id,)).getField('name');
        filename = self.setupPath + '/panel/vhost/nginx/' + siteName + '.conf';
        conf = public.readFile(filename);
        
        #设置共享内存
        oldLimit = self.setupPath + '/panel/vhost/nginx/limit.conf';
        if(os.path.exists(oldLimit)): os.remove(oldLimit);
        limit = self.setupPath + '/nginx/conf/nginx.conf';
        nginxConf = public.readFile(limit);
        limitConf = "limit_conn_zone $binary_remote_addr zone=perip:10m;\n\t\tlimit_conn_zone $server_name zone=perserver:10m;";
        nginxConf = nginxConf.replace("#limit_conn_zone $binary_remote_addr zone=perip:10m;",limitConf);
        public.writeFile(limit,nginxConf)
        
        if(conf.find('limit_conn perserver') != -1):
            #替换总并发
            rep = "limit_conn\s+perserver\s+([0-9]+);";
            conf = re.sub(rep,perserver,conf);
            
            #替换IP并发限制
            rep = "limit_conn\s+perip\s+([0-9]+);";
            conf = re.sub(rep,perip,conf);
            
            #替换请求流量限制
            rep = "limit_rate\s+([0-9]+)\w+;";
            conf = re.sub(rep,limit_rate,conf);
        else:
            conf = conf.replace('#error_page 404/404.html;',"#error_page 404/404.html;\n    " + perserver + "\n    " + perip + "\n    " + limit_rate);
        
        
        import shutil
        shutil.copyfile(filename, '/tmp/backup.conf')
        public.writeFile(filename,conf)
        isError = public.checkWebConfig();
        if(isError != True):
            shutil.copyfile('/tmp/backup.conf',filename)
            return public.returnMsg(False,'ERROR: <br><a style="color:red;">'+isError.replace("\n",'<br>')+'</a>');
        
        public.serviceReload();
        public.WriteLog('TYPE_SITE','SITE_NETLIMIT_OPEN_SUCCESS',(siteName,))
        return public.returnMsg(True, 'SET_SUCCESS');
    
    
    #关闭流量限制
    def CloseLimitNet(self,get):
        id = get.id
        #取回配置文件
        siteName = public.M('sites').where("id=?",(id,)).getField('name');
        filename = self.setupPath + '/panel/vhost/nginx/' + siteName + '.conf';
        conf = public.readFile(filename);
        #清理总并发
        rep = "\s+limit_conn\s+perserver\s+([0-9]+);";
        conf = re.sub(rep,'',conf);
        
        #清理IP并发限制
        rep = "\s+limit_conn\s+perip\s+([0-9]+);";
        conf = re.sub(rep,'',conf);
        
        #清理请求流量限制
        rep = "\s+limit_rate\s+([0-9]+)\w+;";
        conf = re.sub(rep,'',conf);
        public.writeFile(filename,conf)
        public.serviceReload();
        public.WriteLog('TYPE_SITE','SITE_NETLIMIT_CLOSE_SUCCESS',(siteName,))
        return public.returnMsg(True, 'SITE_NETLIMIT_CLOSE_SUCCESS');
    
    #取301配置状态
    def Get301Status(self,get):
        siteName = get.siteName
        result = {}
        domains = ''
        id = public.M('sites').where("name=?",(siteName,)).getField('id')
        tmp = public.M('domain').where("pid=?",(id,)).field('name').select()
        for key in tmp:
            domains += key['name'] + ','
        try:
            if(web.ctx.session.webserver == 'nginx'):
                conf = public.readFile(self.setupPath + '/panel/vhost/nginx/' + siteName + '.conf');
                if conf.find('301-START') == -1:
                    result['domain'] = domains[:-1]
                    result['src'] = "";
                    result['status'] = False
                    result['url'] = "http://";
                    return result;
                rep = "return\s+301\s+((http|https)\://.+);";
                arr = re.search(rep, conf).groups()[0];
                rep = "'\^((\w+\.)+\w+)'";
                tmp = re.search(rep, conf);
                src = ''
                if tmp : src = tmp.groups()[0]
            else:
                conf = public.readFile(self.setupPath + '/panel/vhost/apache/' + siteName + '.conf');
                if conf.find('301-START') == -1:
                    result['domain'] = domains[:-1]
                    result['src'] = "";
                    result['status'] = False
                    result['url'] = "http://";
                    return result;
                rep = "RewriteRule\s+.+\s+((http|https)\://.+)\s+\[";
                arr = re.search(rep, conf).groups()[0];
                rep = "\^((\w+\.)+\w+)\s+\[NC";
                tmp = re.search(rep, conf);
                src = ''
                if tmp : src = tmp.groups()[0]
        except:
            src = ''
            arr = 'http://'
            
        result['domain'] = domains[:-1]
        result['src'] = src.replace("'", '');
        result['status'] = True
        if(len(arr) < 3): result['status'] = False
        result['url'] = arr;
        
        return result
    
    
    #设置301配置
    def Set301Status(self,get):
        siteName = get.siteName
        srcDomain = get.srcDomain
        toDomain = get.toDomain
        type = get.type
        rep = "(http|https)\://.+";
        if not re.match(rep, toDomain):    return public.returnMsg(False,'Url地址不正确!');
        
        
        #nginx
        filename = self.setupPath + '/panel/vhost/nginx/' + siteName + '.conf';
        mconf = public.readFile(filename);
        if mconf:
            if(srcDomain == 'all'):
                conf301 = "\t#301-START\n\t\treturn 301 "+toDomain+"$request_uri;\n\t#301-END";
            else:
                conf301 = "\t#301-START\n\t\tif ($host ~ '^"+srcDomain+"'){\n\t\t\treturn 301 "+toDomain+"$request_uri;\n\t\t}\n\t#301-END";
            if type == '1': 
                mconf = mconf.replace("#error_page 404/404.html;","#error_page 404/404.html;\n"+conf301)
            else:
                rep = "\s+#301-START(.|\n){1,300}#301-END";
                mconf = re.sub(rep, '', mconf);
            
            public.writeFile(filename,mconf)
        
        
        #apache
        filename = self.setupPath + '/panel/vhost/apache/' + siteName + '.conf';
        mconf = public.readFile(filename);
        if type == '1': 
            if(srcDomain == 'all'):
                conf301 = "\n\t#301-START\n\t<IfModule mod_rewrite.c>\n\t\tRewriteEngine on\n\t\tRewriteRule ^(.*)$ "+toDomain+" [L,R=301]\n\t</IfModule>\n\t#301-END\n";
            else:
                conf301 = "\n\t#301-START\n\t<IfModule mod_rewrite.c>\n\t\tRewriteEngine on\n\t\tRewriteCond %{HTTP_HOST} ^"+srcDomain+" [NC]\n\t\tRewriteRule ^(.*) "+toDomain+" [L,R=301]\n\t</IfModule>\n\t#301-END\n";
            rep = "combined"
            mconf = mconf.replace(rep,rep + "\n\t" + conf301);
        else:
            rep = "\n\s+#301-START(.|\n){1,300}#301-END\n*";
            mconf = re.sub(rep, '\n\n', mconf,1);
            mconf = re.sub(rep, '\n\n', mconf,1);
        
        public.writeFile(filename,mconf)
        
        
        isError = public.checkWebConfig();
        if(isError != True):
            shutil.copyfile('/tmp/backup.conf',filename)
            return public.returnMsg(False,'ERROR: <br><a style="color:red;">'+isError.replace("\n",'<br>')+'</a>');
        
        public.serviceReload();
        return public.returnMsg(True,'SUCCESS');
    
    #取子目录绑定
    def GetDirBinding(self,get):
        path = public.M('sites').where('id=?',(get.id,)).getField('path')
        if not os.path.exists(path): 
            checks = ['/','/usr','/etc']
            if path in checks: 
                data = {}
                data['dirs'] = []
                data['binding'] = []
                return data;
            os.system('mkdir -p ' + path);
            os.system('chown 755 ' + path);
        dirnames = []
        for filename in os.listdir(path):
            try:
                filePath = path + '/' + filename
                if os.path.islink(filePath): continue
                if os.path.isdir(filePath):
                    dirnames.append(filename)
            except:
                pass
        
        data = {}
        data['dirs'] = dirnames
        data['binding'] = public.M('binding').where('pid=?',(get.id,)).field('id,pid,domain,path,port,addtime').select()
        return data
    
    #添加子目录绑定
    def AddDirBinding(self,get):
        import shutil
        id = get.id
        tmp = get.domain.split(':')
        domain = tmp[0];
        port = '80'
        if len(tmp) > 1: port = tmp[1];
        if not hasattr(get,'dirName'): public.returnMsg(False, 'DIR_EMPTY');
        dirName = get.dirName; 
        
        reg = "^([\w\-\*]{1,100}\.){1,4}(\w{1,10}|\w{1,10}\.\w{1,10})$";
        if not re.match(reg, domain): return public.returnMsg(False,'SITE_ADD_ERR_DOMAIN');
        
        siteInfo = public.M('sites').where("id=?",(id,)).field('id,path,name').find();
        webdir = siteInfo['path'] + '/' + dirName;
        sql = public.M('binding');
        if sql.where("domain=?",(domain,)).count() > 0: return public.returnMsg(False, 'SITE_ADD_ERR_DOMAIN_EXISTS');
        if public.M('domain').where("name=?",(domain,)).count() > 0: return public.returnMsg(False, 'SITE_ADD_ERR_DOMAIN_EXISTS');
        
        filename = self.setupPath + '/panel/vhost/nginx/' + siteInfo['name'] + '.conf';
        conf = public.readFile(filename);
        if conf:
            rep = "enable-php-([0-9]{2,3})\.conf";
            tmp = re.search(rep,conf).groups()
            version = tmp[0];
            bindingConf ='''
#BINDING-%s-START
server
{
    listen %s;
    server_name %s;
    index index.php index.html index.htm default.php default.htm default.html;
    root %s;
    
    include enable-php-%s.conf;
    include %s/panel/vhost/rewrite/%s.conf;
    location ~ .*\\.(gif|jpg|jpeg|png|bmp|swf)$
    {
        expires      30d;
        access_log off; 
    }
    location ~ .*\\.(js|css)?$
    {
        expires      12h;
        access_log off; 
    }
    access_log %s.log;
}
#BINDING-%s-END''' % (domain,port,domain,webdir,version,self.setupPath,siteInfo['name'],web.ctx.session.logsPath+'/'+siteInfo['name'],domain)
            
            conf += bindingConf
            if web.ctx.session.webserver == 'nginx':
                shutil.copyfile(filename, '/tmp/backup.conf')
            public.writeFile(filename,conf)
            
            
            
        filename = self.setupPath + '/panel/vhost/apache/' + siteInfo['name'] + '.conf';
        conf = public.readFile(filename);
        if conf:
            try:
                try:
                    httpdVersion = public.readFile(self.setupPath+'/apache/version.pl').strip();
                except:
                    httpdVersion = "";
                if httpdVersion == '2.2':
                    phpConfig = "";
                    apaOpt = "Order allow,deny\n\t\tAllow from all";
                else:
                    rep = "php-cgi-([0-9]{2,3})\.sock";
                    tmp = re.search(rep,conf).groups()
                    version = tmp[0];
                    phpConfig ='''
    #PHP     
    <FilesMatch \\.php>
        SetHandler "proxy:unix:/tmp/php-cgi-%s.sock|fcgi://localhost"
    </FilesMatch>
    ''' % (version,)
                    apaOpt = 'Require all granted';
            
                bindingConf ='''
\n#BINDING-%s-START
<VirtualHost *:%s>
    ServerAdmin webmaster@example.com
    DocumentRoot "%s"
    ServerName %s
    errorDocument 404 /404.html
    ErrorLog "%s-error_log"
    CustomLog "%s-access_log" combined
    %s  
    #PATH
    <Directory "%s">
        SetOutputFilter DEFLATE
        Options FollowSymLinks
        AllowOverride All
        %s
        DirectoryIndex index.php index.html index.htm default.php default.html default.htm
    </Directory>
</VirtualHost>
#BINDING-%s-END''' % (domain,port,webdir,domain,web.ctx.session.logsPath+'/'+siteInfo['name'],web.ctx.session.logsPath+'/'+siteInfo['name'],phpConfig,webdir,apaOpt,domain)
                
                conf += bindingConf;
                if web.ctx.session.webserver == 'apache':
                    shutil.copyfile(filename, '/tmp/backup.conf')
                public.writeFile(filename,conf)
            except:
                pass
        
        #检查配置是否有误
        isError = public.checkWebConfig()
        if isError != True:
            shutil.copyfile('/tmp/backup.conf',filename)
            return public.returnMsg(False,'ERROR: <br><a style="color:red;">'+isError.replace("\n",'<br>')+'</a>');
            
        public.M('binding').add('pid,domain,port,path,addtime',(id,domain,port,dirName,public.getDate()));
        public.serviceReload();
        public.WriteLog('TYPE_SITE', 'SITE_BINDING_ADD_SUCCESS',(siteInfo['name'],dirName,domain));
        return public.returnMsg(True, 'ADD_SUCCESS');
    
    #删除子目录绑定
    def DelDirBinding(self,get):
        id = get.id
        binding = public.M('binding').where("id=?",(id,)).field('id,pid,domain,path').find();
        siteName = public.M('sites').where("id=?",(binding['pid'],)).getField('name');
        
        #nginx
        filename = self.setupPath + '/panel/vhost/nginx/' + siteName + '.conf';
        conf = public.readFile(filename);
        if conf:
            rep = "\s*.+BINDING-" + binding['domain'] + "-START(.|\n)+BINDING-" + binding['domain'] + "-END";
            conf = re.sub(rep, '', conf);
            public.writeFile(filename,conf)
        
        #apache
        filename = self.setupPath + '/panel/vhost/apache/' + siteName + '.conf';
        conf = public.readFile(filename);
        if conf:
            rep = "\s*.+BINDING-" + binding['domain'] + "-START(.|\n)+BINDING-" + binding['domain'] + "-END";
            conf = re.sub(rep, '', conf);
            public.writeFile(filename,conf)
        
        public.M('binding').where("id=?",(id,)).delete();
        filename = self.setupPath + '/panel/vhost/rewrite/' + siteName + '_' + binding['path'] + '.conf';
        if os.path.exists(filename): os.remove(filename)
        public.serviceReload();
        public.WriteLog('TYPE_SITE', 'SITE_BINDING_DEL_SUCCESS',(siteName,binding['path']));
        return public.returnMsg(True,'DEL_SUCCESS')
    
    #取默认文档
    #取子目录Rewrite
    def GetDirRewrite(self,get):
        id = get.id;
        find = public.M('binding').where("id=?",(id,)).field('id,pid,domain,path').find();
        site = public.M('sites').where("id=?",(find['pid'],)).field('id,name,path').find();
        
        if(web.ctx.session.webserver == 'apache'):
            filename = site['path']+'/'+find['path']+'/.htaccess';
        else:
            filename = self.setupPath + '/panel/vhost/rewrite/'+site['name']+'_'+find['path']+'.conf';
        
        if hasattr(get,'add'):
            public.writeFile(filename,'')
            if web.ctx.session.webserver == 'nginx':
                file = self.setupPath + '/panel/vhost/nginx/'+site['name']+'.conf';
                conf = public.readFile(file);
                domain = find['domain'];
                rep = "\n#BINDING-"+domain+"-START(.|\n)+BINDING-"+domain+"-END";
                tmp = re.search(rep, conf).group();
                dirConf = tmp.replace('rewrite/'+site['name']+'.conf;', 'rewrite/'+site['name']+'_'+find['path']+'.conf;');
                conf = conf.replace(tmp, dirConf);
                public.writeFile(file,conf)
        data = {}
        data['status'] = False;
        if os.path.exists(filename):
            data['status'] = True;
            data['data'] = public.readFile(filename);
            data['rlist'] = []
            for ds in os.listdir('rewrite/' + web.ctx.session.webserver):
                if ds == 'list.txt': continue;
                data['rlist'].append(ds[0:len(ds)-5]);
            data['filename'] = filename;
        return data
    
    #取默认文档
    def GetIndex(self,get):
        id = get.id;
        Name = public.M('sites').where("id=?",(id,)).getField('name');
        file = self.setupPath + '/panel/vhost/'+web.ctx.session.webserver+'/' + Name + '.conf';
        conf = public.readFile(file)
        if web.ctx.session.webserver == 'nginx':
            rep = "\s+index\s+(.+);";
        else:
            rep = "DirectoryIndex\s+(.+)\n";
            
        tmp = re.search(rep,conf).groups()
        return tmp[0].replace(' ',',')
    
    #设置默认文档
    def SetIndex(self,get):
        id = get.id;
        if get.Index.find('.') == -1: return public.returnMsg(False,  'SITE_INDEX_ERR_FORMAT')
        
        Index = get.Index.replace(' ', '')
        Index = get.Index.replace(',,', ',')
        
        if len(Index) < 3: return public.returnMsg(False,  'SITE_INDEX_ERR_EMPTY')
        
        
        Name = public.M('sites').where("id=?",(id,)).getField('name');
        #准备指令
        Index_L = Index.replace(",", " ");
        
        #nginx
        file = self.setupPath + '/panel/vhost/nginx/' + Name + '.conf';
        conf = public.readFile(file);
        if conf:
            rep = "\s+index\s+.+;";
            conf = re.sub(rep,"\n\tindex " + Index_L + ";",conf);
            public.writeFile(file,conf);
        
        #apache
        file = self.setupPath + '/panel/vhost/apache/' + Name + '.conf';
        conf = public.readFile(file);
        if conf:
            rep = "DirectoryIndex\s+.+\n";
            conf = re.sub(rep,'DirectoryIndex ' + Index_L + "\n",conf);
            public.writeFile(file,conf);
        
        public.serviceReload();
        public.WriteLog('TYPE_SITE', 'SITE_INDEX_SUCCESS',(Name,Index_L));
        return public.returnMsg(True,  'SET_SUCCESS')
    
    #修改物理路径
    def SetPath(self,get):
        id = get.id
        Path = self.GetPath(get.path);
        if Path == "" or id == '0': return public.returnMsg(False,  "DIR_EMPTY");
        
        import files
        if not files.files().CheckDir(Path): return public.returnMsg(False,  "PATH_ERROR");
        
        SiteFind = public.M("sites").where("id=?",(id,)).field('path,name').find();
        if SiteFind["path"] == Path: return public.returnMsg(False,  "SITE_PATH_ERR_RE");
        Name = SiteFind['name'];
        file = self.setupPath + '/panel/vhost/nginx/' + Name + '.conf';
        conf = public.readFile(file);
        if conf:
            conf = conf.replace(SiteFind['path'],Path );
            public.writeFile(file,conf);
        
        file = self.setupPath + '/panel/vhost/apache/' + Name + '.conf';
        conf = public.readFile(file);
        if conf:
            rep = "DocumentRoot\s+.+\n";
            conf = re.sub(rep,'DocumentRoot "' + Path + '"\n',conf);
            rep = "<Directory\s+.+\n";
            conf = re.sub(rep,'<Directory "' + Path + "\">\n",conf);
            public.writeFile(file,conf);
        
        #创建basedir
        userIni = Path + '/.user.ini'
        if not os.path.exists(userIni):
            public.writeFile(userIni, 'open_basedir='+Path+'/:/tmp/:/proc/')
            public.ExecShell('chmod 644 ' + userIni)
            public.ExecShell('chown root:root ' + userIni)
            public.ExecShell('chattr +i '+userIni)
        
        public.serviceReload();
        public.M("sites").where("id=?",(id,)).setField('path',Path);
        public.WriteLog('TYPE_SITE', 'SITE_PATH_SUCCESS',(Name,));
        return public.returnMsg(True,  "SET_SUCCESS");
    
    #取当前可用PHP版本
    def GetPHPVersion(self,get):
        phpVersions = ('52','53','54','55','56','70','71','72','73','74')
        httpdVersion = "";
        filename = self.setupPath+'/apache/version.pl';
        if os.path.exists(filename): httpdVersion = public.readFile(filename).strip()
        
        if httpdVersion == '2.2': phpVersions = ('52','53','54')
        if httpdVersion == '2.4': phpVersions = ('53','54','55','56','70','71','72','73','74')
        
        data = []
        for val in phpVersions:
            tmp = {}
            checkPath = self.setupPath+'/php/'+val+'/bin/php';
            if httpdVersion == '2.2': checkPath = self.setupPath+'/php/'+val+'/libphp5.so';
            if os.path.exists(checkPath):
                tmp['version'] = val;
                tmp['name'] = 'PHP-'+val;
                data.append(tmp)

        return data
    
    
    #取指定站点的PHP版本
    def GetSitePHPVersion(self,get):
        try:
            siteName = get.siteName;
            conf = public.readFile(self.setupPath + '/panel/vhost/'+web.ctx.session.webserver+'/'+siteName+'.conf');
            if web.ctx.session.webserver == 'nginx':
                rep = "enable-php-([0-9]{2,3})\.conf"
            else:
                rep = "php-cgi-([0-9]{2,3})\.sock";
            tmp = re.search(rep,conf).groups()
            data = {}
            data['phpversion'] = tmp[0];
            data['tomcat'] = conf.find('#TOMCAT-START');
            data['tomcatversion'] = public.readFile(self.setupPath + '/tomcat/version.pl');
            data['nodejs'] = conf.find('#NODE.JS-START');
            data['nodejsversion'] = public.readFile(self.setupPath + '/node.js/version.pl');
            return data;
        except:
            return public.returnMsg(False,'SITE_PHPVERSION_ERR_A22');
    
    #设置指定站点的PHP版本
    def SetPHPVersion(self,get):
        siteName = get.siteName
        version = get.version
        
        #nginx
        file = self.setupPath + '/panel/vhost/nginx/'+siteName+'.conf';
        conf = public.readFile(file);
        if conf:
            rep = "enable-php-([0-9]{2,3})\.conf";
            tmp = re.search(rep,conf).group()
            conf = conf.replace(tmp,'enable-php-'+version+'.conf');
            public.writeFile(file,conf)
        
        #apache
        file = self.setupPath + '/panel/vhost/apache/'+siteName+'.conf';
        conf = public.readFile(file);
        if conf:
            rep = "php-cgi-([0-9]{2,3})\.sock";
            tmp = re.search(rep,conf).group()
            conf = conf.replace(tmp,'php-cgi-'+version+'.sock');
            public.writeFile(file,conf)
        
        public.serviceReload();
        public.WriteLog("TYPE_SITE", "SITE_PHPVERSION_SUCCESS",(siteName,version));
        return public.returnMsg(True,'SITE_PHPVERSION_SUCCESS',(siteName,version));

    
    #是否开启目录防御
    def GetDirUserINI(self,get):
        path = get.path;
        id = get.id;
        get.name = public.M('sites').where("id=?",(id,)).getField('name');
        data = {}
        data['logs'] = self.GetLogsStatus(get);
        data['userini'] = False;
        if os.path.exists(path+'/.user.ini'):
            data['userini'] = True;
        data['runPath'] = self.GetSiteRunPath(get);
        data['pass'] = self.GetHasPwd(get);
        return data;

    #设置目录防御
    def SetDirUserINI(self,get):
        path = get.path
        filename = path+'/.user.ini';
        if os.path.exists(filename):
            public.ExecShell("chattr -i "+filename);
            os.remove(filename)
            return public.returnMsg(True, 'SITE_BASEDIR_CLOSE_SUCCESS');
        public.writeFile(filename, 'open_basedir='+path+'/:/tmp/:/proc/');
        public.ExecShell("chattr +i "+filename);
        return public.returnMsg(True,'SITE_BASEDIR_OPEN_SUCCESS');

    #取反向代理
    def GetProxy(self,get):
        name = get.name
        data = {}
        data['status'] = False;
        data['proxyUrl'] = "http://";
        data['toDomain'] = '$host';
        data['sub1'] = '';
        data['sub2'] = '';
        if web.ctx.session.webserver != 'nginx': 
            file = self.setupPath + "/panel/vhost/apache/"+name+".conf";
            conf = public.readFile(file);
            if conf.find('PROXY-START') == -1: return data;
            rep = "ProxyPass\s+/\w*\s+(.+)/";
            tmp = re.search(rep, conf);
            data['proxyUrl'] = "http://"
            if tmp: data['proxyUrl'] = tmp.groups()[0];
            data['toDomain'] = '$host';
            if data['proxyUrl']: data['status'] = True
            
            rep = "\/bin\/sed\s+'s,(.+),(.+),g'";
            tmp = re.search(rep, conf);
            if tmp:
                data['sub1'] = tmp.groups()[0];
                data['sub2'] = tmp.groups()[1];
            
            data['cache'] = False;
            return data;
        
        file = self.setupPath + "/panel/vhost/nginx/"+name+".conf";
        conf = public.readFile(file);
        if conf.find('PROXY-START') == -1: return data;
        
        rep = "proxy_pass\s+(.+);";
        tmp = re.search(rep, conf);
        data['proxyUrl'] = "http://"
        if tmp: data['proxyUrl'] = tmp.groups()[0];
        
        rep = "proxy_set_header\s+Host\s+(.+);";
        tmp = re.search(rep, conf);
        data['toDomain'] = '$host';
        if tmp: data['toDomain'] = tmp.groups()[0];
        rep = "sub_filter \"(.+)\" \"(.+)\";"
        tmp = re.search(rep, conf);
        if tmp:
            data['sub1'] = tmp.groups()[0];
            data['sub2'] = tmp.groups()[1];

        data['status'] = False;
        data['cache'] = False;
        if conf.find('#proxy_cache') == -1: data['cache'] = True;
        if data['proxyUrl']: data['status'] = True
        return data;
    
    
    #设置反向代理
    def SetProxy(self,get):
        name = get.name;
        type = get.type;
        proxyUrl = get.proxyUrl
        rep = "(http|https)\://.+";
        if not re.match(rep, proxyUrl): return public.returnMsg(False,'SITE_PROXY_ERR_URL');
        
        #if get.toDomain != '$host':
        #    rep = "^([\w\-\*]{1,100}\.){1,4}(\w{1,10}|\w{1,10}\.\w{1,10})$";
        #    if not re.match(rep, get.toDomain): return public.returnMsg(False,'SITE_PROXY_ERR_HOST');
        #else:
        #    try:
        #        get.toDomain = re.search('(\w+\.)+\w+',get.proxyUrl).group();
        #    except:
        #        pass
        
        #配置Nginx
        file = self.setupPath + "/panel/vhost/nginx/" + name + ".conf";
        if os.path.exists(file):
            self.CheckProxy(get);
            conf = public.readFile(file);
            if(type == "1"):
                sub_filter = '';
                if get.sub1 != '':
                    sub_filter = '''proxy_set_header Accept-Encoding "";
        sub_filter "%s" "%s";
        sub_filter_once off;''' % (get.sub1,get.sub2)
                
                cureCache = '';
                if os.path.exists('/www/server/nginx/src/ngx_cache_purge'):
                    cureCache = '''
    location ~ /purge(/.*) { 
        proxy_cache_purge cache_one %s$request_uri$is_args$args;
        #access_log  /www/wwwlogs/%s_purge_cache.log;
    }''' % (get.toDomain,name)
                
                proxy='''#PROXY-START%s
    location / 
    {
        proxy_pass %s;
        proxy_set_header Host %s;
        proxy_set_header X-Forwarded-For $remote_addr;
        #proxy_cache cache_one;
        #proxy_cache_key %s$request_uri$is_args$args;
        #proxy_cache_valid 200 304 301 302 1h;
        add_header X-Cache $upstream_cache_status;
        %s
        expires 12h;
    }
    
    location ~ .*\\.(php|jsp|cgi|asp|aspx|flv|swf|xml)?$
    { 
        proxy_set_header Host %s;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_pass %s;
        %s
    }
    #PROXY-END''' % (cureCache,proxyUrl,get.toDomain,get.toDomain,sub_filter,get.toDomain,proxyUrl,sub_filter)
                rep = "location(.|\n)+access_log\s+/"
                conf = re.sub(rep, 'access_log  /', conf)
                conf = conf.replace("include enable-php-", proxy+"\n\n\tinclude enable-php-")
            else:
                rep = "\n\s+#PROXY-START(.|\n){1,1200}#PROXY-END"
                oldconf = '''location ~ .*\\.(gif|jpg|jpeg|png|bmp|swf)$
    {
        expires      30d;
        access_log off; 
    }
    location ~ .*\\.(js|css)?$
    {
        expires      12h;
        access_log off; 
    }'''
                conf = re.sub(rep, '', conf)
                conf = conf.replace('access_log',oldconf + "\n\taccess_log");
            public.writeFile(file,conf)
                
        #APACHE
        file = self.setupPath + "/panel/vhost/apache/"+name+".conf";
        if os.path.exists(file):
            conf = public.readFile(file);
            if(type == "1"):
                sub_filter = '';
                if get.sub1 != '':
                    sub_filter = '''RequestHeader unset Accept-Encoding
        ExtFilterDefine fixtext mode=output intype=text/html cmd="/bin/sed 's,%s,%s,g'"
        SetOutputFilter fixtext''' % (get.sub1,get.sub2)
                proxy = '''#PROXY-START
    <IfModule mod_proxy.c>
        ProxyRequests Off
        SSLProxyEngine on
        ProxyPass / %s/
        ProxyPassReverse / %s/
        %s
    </IfModule>
    #PROXY-END''' % (proxyUrl,proxyUrl,sub_filter)
                rep = "combined"
                conf = conf.replace(rep,rep + "\n\n\t" + proxy);
            else:
                rep = "\n\s+#PROXY-START(.|\n){1,400}#PROXY-END"
                conf = re.sub(rep, '', conf)
            public.writeFile(file,conf)
        
        public.serviceReload()
        return public.returnMsg(True, 'SUCCESS')
    
    
    #开启缓存
    def ProxyCache(self,get):
        if web.ctx.session.webserver != 'nginx': return public.returnMsg(False,'WAF_NOT_NGINX');
        file = self.setupPath + "/panel/vhost/nginx/"+get.siteName+".conf";
        conf = public.readFile(file);
        if conf.find('proxy_pass') == -1: return public.returnMsg(False,'SET_ERROR');
        if conf.find('#proxy_cache') != -1:
            conf = conf.replace('#proxy_cache','proxy_cache');
            conf = conf.replace('#expires 12h','expires 12h');
        else:
            conf = conf.replace('proxy_cache','#proxy_cache');
            conf = conf.replace('expires 12h','#expires 12h');
        
        public.writeFile(file,conf);
        public.serviceReload();
        return public.returnMsg(True,'SET_SUCCESS');
    
    
    #检查反向代理配置
    def CheckProxy(self,get):
        if web.ctx.session.webserver != 'nginx': return True;
        file = self.setupPath + "/nginx/conf/proxy.conf";
        if not os.path.exists(file):
            conf='''proxy_temp_path %s/nginx/proxy_temp_dir;
    proxy_cache_path %s/nginx/proxy_cache_dir levels=1:2 keys_zone=cache_one:10m inactive=1d max_size=5g;
    client_body_buffer_size 512k;
    proxy_connect_timeout 60;
    proxy_read_timeout 60;
    proxy_send_timeout 60;
    proxy_buffer_size 32k;
    proxy_buffers 4 64k;
    proxy_busy_buffers_size 128k;
    proxy_temp_file_write_size 128k;
    proxy_next_upstream error timeout invalid_header http_500 http_503 http_404;
    proxy_cache cache_one;''' % (self.setupPath,self.setupPath)
            public.writeFile(file,conf)
        
        
        file = self.setupPath + "/nginx/conf/nginx.conf";
        conf = public.readFile(file);
        if(conf.find('include proxy.conf;') == -1):
            rep = "include\s+mime.types;";
            conf = re.sub(rep, "include mime.types;\n\tinclude proxy.conf;", conf);
            public.writeFile(file,conf)
        
    
    #取伪静态规则应用列表
    def GetRewriteList(self,get):
        rewriteList = {}
        if web.ctx.session.webserver == 'apache': 
            get.id = public.M('sites').where("name=?",(get.siteName,)).getField('id');
            runPath = self.GetSiteRunPath(get);
            rewriteList['sitePath'] = public.M('sites').where("name=?",(get.siteName,)).getField('path') + runPath['runPath'];
            
        rewriteList['rewrite'] = []
        rewriteList['rewrite'].append('0.'+public.getMsg('SITE_REWRITE_NOW'))
        for ds in os.listdir('rewrite/' + web.ctx.session.webserver):
            if ds == 'list.txt': continue;
            rewriteList['rewrite'].append(ds[0:len(ds)-5]);
        rewriteList['rewrite'] = sorted(rewriteList['rewrite']);
        return rewriteList
    
    #保存伪静态模板
    def SetRewriteTel(self,get):
        get.name = get.name.encode('utf-8');
        filename = 'rewrite/' + web.ctx.session.webserver + '/' +get.name + '.conf';
        public.writeFile(filename,get.data[0]);
        return public.returnMsg(True, 'SITE_REWRITE_SAVE');
    
    #打包
    def ToBackup(self,get):
        id = get.id;
        find = public.M('sites').where("id=?",(id,)).field('name,path,id').find();
        import time
        fileName = find['name']+'_'+time.strftime('%Y%m%d_%H%M%S',time.localtime())+'.zip';
        backupPath = web.ctx.session.config['backup_path'] + '/site'
        zipName = backupPath + '/'+fileName;
        if not (os.path.exists(backupPath)): os.makedirs(backupPath)
        tmps = '/tmp/panelExec.log'
        execStr = "cd '" + find['path'] + "' && zip '" + zipName + "' -r ./* > " + tmps + " 2>&1"
        public.ExecShell(execStr)
        sql = public.M('backup').add('type,name,pid,filename,size,addtime',(0,fileName,find['id'],zipName,0,public.getDate()));
        public.WriteLog('TYPE_SITE', 'SITE_BACKUP_SUCCESS',(find['name'],));
        return public.returnMsg(True, 'BACKUP_SUCCESS');
    
    
    #删除备份文件
    def DelBackup(self,get):
        id = get.id
        where = "id=?";
        filename = public.M('backup').where(where,(id,)).getField('filename');
        if os.path.exists(filename): os.remove(filename)
        name = '';
        if filename == 'qiniu':
            name = public.M('backup').where(where,(id,)).getField('name');
            public.ExecShell("python "+self.setupPath + '/panel/script/backup_qiniu.py delete_file ' + name)
        
        public.WriteLog('TYPE_SITE', 'SITE_BACKUP_DEL_SUCCESS',(name,filename));
        public.M('backup').where(where,(id,)).delete();
        return public.returnMsg(True, 'DEL_SUCCESS');
    
    #旧版本配置文件处理
    def OldConfigFile(self):
        #检查是否需要处理
        moveTo = 'data/moveTo.pl';
        if os.path.exists(moveTo): return;
        
        #处理Nginx配置文件
        filename = self.setupPath + "/nginx/conf/nginx.conf"
        if os.path.exists(filename):
            conf = public.readFile(filename);
            if conf.find('include vhost/*.conf;') != -1:
                conf = conf.replace('include vhost/*.conf;','include ' + self.setupPath + '/panel/vhost/nginx/*.conf;');
                public.writeFile(filename,conf);
        
        self.moveConf(self.setupPath + "/nginx/conf/vhost", self.setupPath + '/panel/vhost/nginx','rewrite',self.setupPath+'/panel/vhost/rewrite');
        self.moveConf(self.setupPath + "/nginx/conf/rewrite", self.setupPath + '/panel/vhost/rewrite');
        
        
        
        #处理Apache配置文件
        filename = self.setupPath + "/apache/conf/httpd.conf"
        if os.path.exists(filename):
            conf = public.readFile(filename);
            if conf.find('IncludeOptional conf/vhost/*.conf') != -1:
                conf = conf.replace('IncludeOptional conf/vhost/*.conf','IncludeOptional ' + self.setupPath + '/panel/vhost/apache/*.conf');
                public.writeFile(filename,conf);
        
        self.moveConf(self.setupPath + "/apache/conf/vhost", self.setupPath + '/panel/vhost/apache');
        
        #标记处理记录
        public.writeFile(moveTo,'True');
        public.serviceReload();
        
    #移动旧版本配置文件
    def moveConf(self,Path,toPath,Replace=None,ReplaceTo=None):
        if not os.path.exists(Path): return;
        import shutil
        
        letPath = '/etc/letsencrypt/live';
        nginxPath = self.setupPath + '/nginx/conf/key'
        apachePath = self.setupPath + '/apache/conf/key'
        for filename in os.listdir(Path):
            #准备配置文件
            name = filename[0:len(filename) - 5];
            filename = Path + '/' + filename;
            conf = public.readFile(filename);
            
            #替换关键词
            if Replace: conf = conf.replace(Replace,ReplaceTo);
            ReplaceTo = letPath + name;
            Replace = 'conf/key/' + name;
            if conf.find(Replace) != -1: conf = conf.replace(Replace,ReplaceTo);
            Replace = 'key/' + name;
            if conf.find(Replace) != -1: conf = conf.replace(Replace,ReplaceTo);
            public.writeFile(filename,conf);
            
            #提取配置信息
            if conf.find('server_name') != -1:
                self.formatNginxConf(filename);
            elif conf.find('<Directory') != -1:
                #self.formatApacheConf(filename)
                pass;
            
            #移动文件
            shutil.move(filename, toPath + '/' + name + '.conf');
            
            #转移证书
            self.moveKey(nginxPath + '/' + name, letPath + '/' + name)
            self.moveKey(apachePath + '/' + name, letPath + '/' + name)
        
        #删除多余目录
        shutil.rmtree(Path);
        #重载服务
        public.serviceReload();
        
    #从Nginx配置文件获取站点信息
    def formatNginxConf(self,filename):
        
        #准备基础信息
        name = os.path.basename(filename[0:len(filename) - 5]);
        if name.find('.') == -1: return;
        conf = public.readFile(filename);
        print conf
        #取域名
        rep = "server_name\s+(.+);"
        tmp = re.search(rep,conf);
        if not tmp: return;
        domains = tmp.groups()[0].split(' ');
        print domains
        
        #取根目录
        rep = "root\s+(.+);"
        tmp = re.search(rep,conf);
        if not tmp: return;
        path = tmp.groups()[0];
        
        #提交到数据库
        self.toSiteDatabase(name, domains, path);
    
    #从Apache配置文件获取站点信息
    def formatApacheConf(self,filename):
        #准备基础信息
        name = os.path.basename(filename[0:len(filename) - 5]);
        if name.find('.') == -1: return;
        conf = public.readFile(filename);
        
        #取域名
        rep = "ServerAlias\s+(.+)\n"
        tmp = re.search(rep,conf);
        if not tmp: return;
        domains = tmp.groups()[0].split(' ');
        
        #取根目录
        rep = u"DocumentRoot\s+\"(.+)\"\n"
        tmp = re.search(rep,conf);
        if not tmp: return;
        path = tmp.groups()[0];
        
        #提交到数据库
        self.toSiteDatabase(name, domains, path);
    
    #添加到数据库
    def toSiteDatabase(self,name,domains,path):
        if public.M('sites').where('name=?',(name,)).count() > 0: return;
        public.M('sites').add('name,path,status,ps,addtime',(name,path,'1','请输入备注',public.getDate()));
        pid = public.M('sites').where("name=?",(name,)).getField('id');
        for domain in domains:
            public.M('domain').add('pid,name,port,addtime',(pid,domain,'80',public.getDate()))
    
    #移动旧版本证书
    def moveKey(self,srcPath,dstPath):
        if not os.path.exists(srcPath): return;
        import shutil
        os.makedirs(dstPath);
        srcKey = srcPath + '/key.key';
        srcCsr = srcPath + '/csr.key';
        if os.path.exists(srcKey): shutil.move(srcKey,dstPath + '/privkey.pem');
        if os.path.exists(srcCsr): shutil.move(srcCsr,dstPath + '/fullchain.pem');
    
    #路径处理
    def GetPath(self,path):
        if path[-1] == '/':
            return path[0:-1];
        return path;
    
    #日志开关
    def logsOpen(self,get):
        get.name = public.M('sites').where("id=?",(get.id,)).getField('name');
        # APACHE
        filename = web.ctx.session.setupPath + '/panel/vhost/apache/' + get.name + '.conf';
        if os.path.exists(filename):
            conf = public.readFile(filename);
            if conf.find('#ErrorLog') != -1:
                conf = conf.replace("#ErrorLog","ErrorLog").replace('#CustomLog','CustomLog');
            else:
                conf = conf.replace("ErrorLog","#ErrorLog").replace('CustomLog','#CustomLog');
            public.writeFile(filename,conf);
        
        #NGINX
        filename = web.ctx.session.setupPath + '/panel/vhost/nginx/' + get.name + '.conf';
        if os.path.exists(filename):
            conf = public.readFile(filename);
            rep = web.ctx.session.logsPath + "/"+get.name+".log";
            if conf.find(rep) != -1:
                conf = conf.replace(rep,"off");
            else:
                conf = conf.replace('access_log  off','access_log  ' + rep);
            public.writeFile(filename,conf);
        
        public.serviceReload();
        return public.returnMsg(True, 'SUCCESS');
    
    #取日志状态
    def GetLogsStatus(self,get):
        filename = web.ctx.session.setupPath + '/panel/vhost/'+web.ctx.session.webserver+'/' + get.name + '.conf';
        conf = public.readFile(filename);
        if conf.find('#ErrorLog') != -1: return False;
        if conf.find("access_log  off") != -1: return False;
        return True;
    
    #取目录加密状态
    def GetHasPwd(self,get):
        if not hasattr(get,'siteName'):
            get.siteName = public.M('sites').where('id=?',(get.id,)).getField('name');
            get.configFile = self.setupPath + '/panel/vhost/nginx/' + get.siteName + '.conf';
        conf = public.readFile(get.configFile);
        if conf.find('#AUTH_START') != -1: return True;
        return False;
            
    #设置目录加密
    def SetHasPwd(self,get):
        if not hasattr(get,'siteName'): 
            get.siteName = public.M('sites').where('id=?',(get.id,)).getField('name');
            
        self.CloseHasPwd(get);
        filename = web.ctx.session.setupPath + '/pass/' + get.siteName + '.pass';
        passconf = get.username + ':' + public.hasPwd(get.password);
        
        if get.siteName == 'phpmyadmin': 
            get.configFile = self.setupPath + '/nginx/conf/nginx.conf';
        else:
            get.configFile = self.setupPath + '/panel/vhost/nginx/' + get.siteName + '.conf';
            
        #处理Nginx配置
        conf = public.readFile(get.configFile);
        if conf:
            rep = '#error_page   404   /404.html;';
            if conf.find(rep) == -1: rep = '#error_page 404/404.html;';
            data = '''
    #AUTH_START
    auth_basic "Authorization";
    auth_basic_user_file %s;
    #AUTH_END''' % (filename,)
            conf = conf.replace(rep,rep + data);
            public.writeFile(get.configFile,conf);
        
        
        if get.siteName == 'phpmyadmin': 
            get.configFile = self.setupPath + '/apache/conf/extra/httpd-vhosts.conf';
        else:
            get.configFile = self.setupPath + '/panel/vhost/apache/' + get.siteName + '.conf';
            
        conf = public.readFile(get.configFile);
        if conf:
            #处理Apache配置
            rep = 'SetOutputFilter'
            if conf.find(rep) != -1:
                data = '''#AUTH_START
        AuthType basic
        AuthName "Authorization "
        AuthUserFile %s
        Require user %s
        #AUTH_END
        ''' % (filename,get.username)
                conf = conf.replace(rep,data + rep);
                conf = conf.replace(' Require all granted'," #Require all granted");
                public.writeFile(get.configFile,conf);
          
        #写密码配置  
        passDir = web.ctx.session.setupPath + '/pass';
        if not os.path.exists(passDir): public.ExecShell('mkdir -p ' + passDir)
        public.writeFile(filename,passconf);
        public.serviceReload();
        public.WriteLog("TYPE_SITE","SITE_AUTH_OPEN_SUCCESS",(get.siteName,));
        return public.returnMsg(True,'SET_SUCCESS');
        
    #取消目录加密
    def CloseHasPwd(self,get):
        if not hasattr(get,'siteName'): 
            get.siteName = public.M('sites').where('id=?',(get.id,)).getField('name');
            
        if get.siteName == 'phpmyadmin': 
            get.configFile = self.setupPath + '/nginx/conf/nginx.conf';
        else:
            get.configFile = self.setupPath + '/panel/vhost/nginx/' + get.siteName + '.conf';
        
        if os.path.exists(get.configFile):
            conf = public.readFile(get.configFile);
            rep = "\n\s*#AUTH_START(.|\n){1,200}#AUTH_END";
            conf = re.sub(rep,'',conf);
            public.writeFile(get.configFile,conf);
            
        if get.siteName == 'phpmyadmin': 
            get.configFile = self.setupPath + '/apache/conf/extra/httpd-vhosts.conf';
        else:
            get.configFile = self.setupPath + '/panel/vhost/apache/' + get.siteName + '.conf';
        
        if os.path.exists(get.configFile):
            conf = public.readFile(get.configFile);
            rep = "\n\s*#AUTH_START(.|\n){1,200}#AUTH_END";
            conf = re.sub(rep,'',conf);
            conf = conf.replace(' #Require all granted'," Require all granted");
            public.writeFile(get.configFile,conf);
        public.serviceReload();
        public.WriteLog("TYPE_SITE","SITE_AUTH_CLOSE_SUCCESS",(get.siteName,));
        return public.returnMsg(True,'SET_SUCCESS');
    
    #启用tomcat支持
    def SetTomcat(self,get):
        siteName = get.siteName;
        name = siteName.replace('.','_');
        
        rep = "^(\d{1,3}\.){3,3}\d{1,3}$";
        if re.match(rep,siteName): return public.returnMsg(False,'TOMCAT_IP');
        
        #nginx
        filename = self.setupPath + '/panel/vhost/nginx/' + siteName + '.conf';
        if os.path.exists(filename):
            conf = public.readFile(filename);
            if conf.find('#TOMCAT-START') != -1: return self.CloseTomcat(get);
            tomcatConf = '''#TOMCAT-START
    location /
    {
        proxy_pass "http://%s:8080";
        proxy_set_header Host %s;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
    location ~ .*\.(html|htm|gif|jpg|jpeg|bmp|png|ico|txt|js|css)$
    {
        expires      12h;
    }
    #TOMCAT-END
    ''' % (siteName,siteName)
            rep = 'include enable-php';
            conf = conf.replace(rep,tomcatConf + rep);
            public.writeFile(filename,conf);
        
        #apache
        filename = self.setupPath + '/panel/vhost/apache/' + siteName + '.conf';
        if os.path.exists(filename):
            conf = public.readFile(filename);
            if conf.find('#TOMCAT-START') != -1: return self.CloseTomcat(get);
            tomcatConf = '''#TOMCAT-START
    <IfModule mod_proxy.c>
        ProxyRequests Off
        SSLProxyEngine on
        ProxyPass / http://%s:8080/
        ProxyPassReverse / http://%s:8080/
        RequestHeader unset Accept-Encoding
        ExtFilterDefine fixtext mode=output intype=text/html cmd="/bin/sed 's,:8080,,g'"
        SetOutputFilter fixtext
    </IfModule>
    #TOMCAT-END
    ''' % (siteName,siteName)
            
            rep = '#PATH';
            conf = conf.replace(rep,tomcatConf + rep);
            public.writeFile(filename,conf);
        path = public.M('sites').where("name=?",(siteName,)).getField('path');
        import tomcat
        tomcat.tomcat().AddVhost(path,siteName);
        public.serviceReload();
        public.ExecShell('/etc/init.d/tomcat stop');
        public.ExecShell('/etc/init.d/tomcat start');
        public.ExecShell('echo "127.0.0.1 '+siteName + '" >> /etc/hosts');
        public.WriteLog('TYPE_SITE','SITE_TOMCAT_OPEN',(siteName,))
        return public.returnMsg(True,'SITE_TOMCAT_OPEN');
    
    #关闭tomcat支持
    def CloseTomcat(self,get):
        if not os.path.exists('/etc/init.d/tomcat'): return False;
        siteName = get.siteName;
        name = siteName.replace('.','_');
        
        #nginx
        filename = self.setupPath + '/panel/vhost/nginx/' + siteName + '.conf';
        if os.path.exists(filename):
            conf = public.readFile(filename);
            rep = "\s*#TOMCAT-START(.|\n)+#TOMCAT-END"
            conf = re.sub(rep,'',conf);
            public.writeFile(filename,conf);
        
        #apache
        filename = self.setupPath + '/panel/vhost/apache/' + siteName + '.conf';
        if os.path.exists(filename):
            conf = public.readFile(filename);
            rep = "\s*#TOMCAT-START(.|\n)+#TOMCAT-END"
            conf = re.sub(rep,'',conf);
            public.writeFile(filename,conf);
        
        public.ExecShell('rm -rf ' + self.setupPath + '/panel/vhost/tomcat/' + name);
        try:
            import tomcat
            tomcat.tomcat().DelVhost(siteName);
        except:
            pass
        public.serviceReload();
        public.ExecShell('/etc/init.d/tomcat restart');
        public.ExecShell("sed -i '/"+siteName+"/d' /etc/hosts");
        public.WriteLog('TYPE_SITE','SITE_TOMCAT_CLOSE',(siteName,));
        return public.returnMsg(True,'SITE_TOMCAT_CLOSE');
    
    #取当站点前运行目录
    def GetSiteRunPath(self,get):
        siteName = public.M('sites').where('id=?',(get.id,)).getField('name');
        sitePath = public.M('sites').where('id=?',(get.id,)).getField('path');
        if web.ctx.session.webserver == 'nginx':
            filename = self.setupPath + '/panel/vhost/nginx/' + siteName + '.conf'
            conf = public.readFile(filename)
            rep = '\s*root\s*(.+);'
            path = re.search(rep,conf).groups()[0];
        else:
            filename = self.setupPath + '/panel/vhost/apache/' + siteName + '.conf'
            conf = public.readFile(filename)
            rep = '\s*DocumentRoot\s*"(.+)"\s*\n'
            path = re.search(rep,conf).groups()[0];
        
        data = {}
        if sitePath == path: 
            data['runPath'] = '/';
        else:
            data['runPath'] = path.replace(sitePath,'');
        
        dirnames = []
        dirnames.append('/');
        for filename in os.listdir(sitePath):
            try:
                filePath = sitePath + '/' + filename
                if os.path.islink(filePath): continue
                if os.path.isdir(filePath):
                    dirnames.append('/' + filename)
            except:
                pass
        
        data['dirs'] = dirnames;
        return data;
    
    #设置当前站点运行目录
    def SetSiteRunPath(self,get):
        siteName = public.M('sites').where('id=?',(get.id,)).getField('name');
        sitePath = public.M('sites').where('id=?',(get.id,)).getField('path');
        
        #处理Nginx
        filename = self.setupPath + '/panel/vhost/nginx/' + siteName + '.conf'
        if os.path.exists(filename):
            conf = public.readFile(filename)
            rep = '\s*root\s*(.+);'
            path = re.search(rep,conf).groups()[0];
            conf = conf.replace(path,sitePath + get.runPath);
            public.writeFile(filename,conf);
            
        #处理Apache
        filename = self.setupPath + '/panel/vhost/apache/' + siteName + '.conf'
        if os.path.exists(filename):
            conf = public.readFile(filename)
            rep = '\s*DocumentRoot\s*"(.+)"\s*\n'
            path = re.search(rep,conf).groups()[0];
            conf = conf.replace(path,sitePath + get.runPath);
            public.writeFile(filename,conf);
        
        public.serviceReload();
        return public.returnMsg(True,'SET_SUCCESS');
    
    #设置默认站点
    def SetDefaultSite(self,get):
        import time;
        #清理旧的
        defaultSite = public.readFile('data/defaultSite.pl');
        if defaultSite:
            path = self.setupPath + '/panel/vhost/nginx/' + defaultSite + '.conf';
            if os.path.exists(path):
                conf = public.readFile(path);
                rep = "listen\s+80.+;"
                conf = re.sub(rep,'listen 80;',conf,1);
                public.writeFile(path,conf);

        #处理新的
        path = self.setupPath + '/apache/htdocs';
        if os.path.exists(path):
            conf = '''<IfModule mod_rewrite.c>
  RewriteEngine on
  RewriteRule (.*) http://%s/$1 [L]
</IfModule>''' % (get.name,)
            if get.name == 'off': conf = '';
            public.writeFile(path + '/.htaccess',conf);
            
        
        path = self.setupPath + '/panel/vhost/nginx/' + get.name + '.conf';
        if os.path.exists(path):
            conf = public.readFile(path);
            rep = "listen\s+80\s*;"
            conf = re.sub(rep,'listen 80 default_server;',conf,1);
            rep = "listen\s+443\s*ssl\s*\w*\s*;"
            conf = re.sub(rep,'listen 443 ssl default_server;',conf,1);
            public.writeFile(path,conf);
        
        path = self.setupPath + '/panel/vhost/nginx/default.conf';
        if os.path.exists(path): public.ExecShell('rm -f ' + path);
        public.writeFile('data/defaultSite.pl',get.name);
        public.serviceReload();
        return public.returnMsg(True,'SET_SUCCESS');
    
    #取默认站点
    def GetDefaultSite(self,get):
        data = {}
        data['sites'] = public.M('sites').field('name').order('id desc').select();
        data['defaultSite'] = public.readFile('data/defaultSite.pl');
        return data;
    
    #扫描站点
    def CheckSafe(self,get):
        import db,time
        isTask = '/tmp/panelTask.pl'
        if os.path.exists(self.setupPath + '/panel/class/panelSafe.py'):
            import py_compile
            py_compile.compile(self.setupPath + '/panel/class/panelSafe.py');
        get.path = public.M('sites').where('id=?',(get.id,)).getField('path');
        execstr = "cd " + web.ctx.session.setupPath + "/panel/class && python panelSafe.pyc " + get.path;
        sql = db.Sql()
        sql.table('tasks').add('id,name,type,status,addtime,execstr',(None,'扫描目录 ['+get.path+']','execshell','0',time.strftime('%Y-%m-%d %H:%M:%S'),execstr))
        public.writeFile(isTask,'True')
        public.WriteLog('TYPE_SETUP','SITE_SCAN_ADD',(get.path,));
        return public.returnMsg(True,'SITE_SCAN_ADD');
    
    #获取结果信息
    def GetCheckSafe(self,get):
        get.path = public.M('sites').where('id=?',(get.id,)).getField('path');
        path = get.path + '/scan.pl'
        result = {};
        result['data'] = []
        result['phpini'] = []
        result['userini'] = result['sshd'] = True;
        result['scan'] = False
        result['outime'] = result['count'] = result['error'] = 0
        if not os.path.exists(path): return result;
        import json
        return json.loads(public.readFile(path));
        
    #更新病毒库
    def UpdateRulelist(self,get):
        try:
            conf = public.httpGet(public.getUrl()+'/install/ruleList.conf')
            if conf:
                public.writeFile(self.setupPath + '/panel/data/ruleList.conf',conf);
                return public.returnMsg(True,'UPDATE_SUCCESS');
            return public.returnMsg(False,'CONNECT_ERR');
        except:
            return public.returnMsg(False,'CONNECT_ERR');
    
    #设置到期时间
    def SetEdate(self,get):
        result = public.M('sites').where('id=?',(get.id,)).setField('edate',get.edate);
        siteName = public.M('sites').where('id=?',(get.id,)).getField('name');
        public.WriteLog('TYPE_SITE','SITE_EXPIRE_SUCCESS',(siteName,get.edate));
        return public.returnMsg(True,'SITE_EXPIRE_SUCCESS');
