#!/usr/bin/env python
#coding:utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2016 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <2879625666@qq.com>
# +-------------------------------------------------------------------
import sys,os,public,time
reload(sys)
sys.setdefaultencoding('utf-8')
class files:
    #检查敏感目录
    def CheckDir(self,path):
        import web
        path = path.replace('//','/');
        if path[-1:] == '/':
            path = path[:-1]
        
        nDirs = ('',
                 '/',
                '/*',
                '/www',
                '/root',
                '/boot',
                '/bin',
                '/etc',
                '/home',
                '/dev',
                '/sbin',
                '/var',
                '/usr', 
                '/tmp',
                '/sys',
                '/proc',
                '/media',
                '/mnt',
                '/opt',
                '/lib',
                '/srv', 
                '/selinux',
                '/www/server',
                '/www/server/data',
                web.ctx.session.rootPath,
                web.ctx.session.logsPath,
                web.ctx.session.setupPath)
        for dir in nDirs:
            if(dir == path):
                return False
        return True
    #上传文件
    def UploadFile(self,get):
        get.path = get.path.encode('utf-8');
        if get.path.find(':\\') != -1:
            tmp = get.path.split('\\');
            get.path = tmp[len(tmp)-1];
        try:
            if not os.path.exists(get.path): os.makedirs(get.path);
            filename = (get['path'] + get['zunfile'].filename).encode('utf-8');
            fp = open(filename,'wb');
            fp.write(get['zunfile'].file.read());
            fp.close()
            if(get.codeing != 'byte'):
                srcBody = public.readFile(filename)
                import chardet
                char=chardet.detect(srcBody)
                srcBody = srcBody.decode(char['encoding']).encode('utf-8')
                public.writeFile(filename,srcBody.encode(get.codeing));
            os.system('chown www.www ' + filename);
            public.WriteLog('TYPE_FILE','FILE_UPLOAD_SUCCESS',(get['zunfile'].filename,get['path']))        
            return public.returnMsg(True,'FILE_UPLOAD_SUCCESS')
        except:
            import time
            opt = time.strftime('%Y-%m-%d_%H%M%S',time.localtime())
            tmp = get['zunfile'].filename.split('.');
            if len(tmp) < 2:
                ext = ""
            else:
                ext = "." + tmp[-1];
            filename = get['path'] + "New_uploaded_files_" + opt + ext;
            fp = open(filename.encode('utf-8'),'wb');
            fp.write(get['zunfile'].file.read());
            fp.close()
            os.system('chown www.www ' + filename);
            public.WriteLog('TYPE_FILE','FILE_UPLOAD_SUCCESS',(get['zunfile'].filename,get['path']))
            return public.returnMsg(True,'FILE_UPLOAD_SUCCESS')
        
    #取文件/目录列表
    def GetDir(self,get):
        get.path = get.path.encode('utf-8');
        if not os.path.exists(get.path): get.path = '/www';
        import pwd 
        dirnames = []
        filenames = []
        
        search = None
        if hasattr(get,'search'): search = get.search.strip().lower();
        
        #包含分页类
        import page
        #实例化分页类
        page = page.Page();
        info = {}
        info['count'] = self.GetFilesCount(get.path,search);
        info['row']   = 100
        info['p'] = 1
        if hasattr(get,'p'):
            info['p']     = int(get['p'])
        info['uri']   = {}
        info['return_js'] = ''
        if hasattr(get,'tojs'):
            info['return_js']   = get.tojs
        if hasattr(get,'showRow'):
            info['row'] = int(get.showRow);
        
        #获取分页数据
        data = {}
        data['PAGE'] = page.GetPage(info,'1,2,3,4,5,6,7,8')
        
        
        
        i = 0;
        n = 0;
        for filename in os.listdir(get.path):
            if search:
                if filename.lower().find(search) == -1: continue;
            i += 1;
            if n >= page.ROW: break;
            if i < page.SHIFT: continue;
            
            try:
                filePath = (get.path+'/'+filename).encode('utf8')
                link = '';
                if os.path.islink(filePath): 
                    filePath = os.readlink(filePath);
                    link = ' -> ' + filePath;
                    if not os.path.exists(filePath): filePath = get.path + '/' + filePath;
                    if not os.path.exists(filePath): continue;
                
                stat = os.stat(filePath)
                accept = str(oct(stat.st_mode)[-3:]);
                mtime = str(int(stat.st_mtime))
                user = ''
                try:
                    user = pwd.getpwuid(stat.st_uid).pw_name
                except:
                    user = str(stat.st_uid)
                size = str(stat.st_size)
                if os.path.isdir(filePath):
                    dirnames.append(filename+';'+size+';'+mtime+';'+accept+';'+user+';'+link);
                else:
                    filenames.append(filename+';'+size+';'+mtime+';'+accept+';'+user+';'+link);
                n += 1;
            except:
                continue;
        
        
        data['DIR'] = sorted(dirnames);
        data['FILES'] = sorted(filenames);
        data['PATH'] = get.path
        if hasattr(get,'disk'):
            import system
            data['DISK'] = system.system().GetDiskInfo();
        return data
    
    #计算文件数量
    def GetFilesCount(self,path,search):
        i=0;
        for name in os.listdir(path):
            if search:
                if name.lower().find(search) == -1: continue;
            i += 1;
        return i;
    
    #创建文件
    def CreateFile(self,get):
        get.path = get.path.encode('utf-8');
        try:
            if os.path.exists(get.path):
                return public.returnMsg(False,'FILE_EXISTS')
            
            path = os.path.dirname(get.path)
            if not os.path.exists(path):
                os.makedirs(path)
            open(get.path,'w+').close()
            self.SetFileAccept(get.path);
            public.WriteLog('TYPE_FILE','FILE_CREATE_SUCCESS',(get.path,))
            return public.returnMsg(True,'FILE_CREATE_SUCCESS')
        except:
            return public.returnMsg(False,'FILE_CREATE_ERR')
    
    #创建目录
    def CreateDir(self,get):
        get.path = get.path.encode('utf-8');
        try:
            if os.path.exists(get.path):
                return public.returnMsg(False,'DIR_EXISTS')
            os.makedirs(get.path)
            self.SetFileAccept(get.path);
            public.WriteLog('TYPE_FILE','DIR_CREATE_SUCCESS',(get.path,))
            return public.returnMsg(True,'DIR_CREATE_SUCCESS')
        except:
            return public.returnMsg(False,'DIR_CREATE_ERR')
    
    
    #删除目录
    def DeleteDir(self,get) :
        get.path = get.path.encode('utf-8');
        #if get.path.find('/www/wwwroot') == -1: return public.returnMsg(False,'此为演示服务器,禁止删除此目录!');
        if not os.path.exists(get.path):
            return public.returnMsg(False,'DIR_NOT_EXISTS')
        
        #检查是否敏感目录
        if not self.CheckDir(get.path):
            return public.returnMsg(False,'FILE_DANGER');
        
        try:
            #检查是否存在.user.ini
            if os.path.exists(get.path+'/.user.ini'):
                os.system("chattr -i '"+get.path+"/.user.ini'")
            if hasattr(get,'empty'):
                if not self.delete_empty(get.path): return public.returnMsg(False,'DIR_ERR_NOT_EMPTY');
            
            if os.path.exists('data/recycle_bin.pl'):
                if self.Mv_Recycle_bin(get): return public.returnMsg(True,'DIR_MOVE_RECYCLE_BIN');
            
            import shutil
            shutil.rmtree(get.path)
            public.WriteLog('TYPE_FILE','DIR_DEL_SUCCESS',(get.path,))
            return public.returnMsg(True,'DIR_DEL_SUCCESS')
        except:
            return public.returnMsg(False,'DIR_DEL_ERR')
    
    #删除 空目录 
    def delete_empty(self,path):
        get.path = get.path.encode('utf-8');
        for files in os.listdir(path):
            return False
        return True
    
    #删除文件
    def DeleteFile(self,get):
        get.path = get.path.encode('utf-8');
        #if get.path.find('/www/wwwroot') == -1: return public.returnMsg(False,'此为演示服务器,禁止删除此文件!');
        if not os.path.exists(get.path):
            return public.returnMsg(False,'FILE_NOT_EXISTS')
        
        #检查是否为.user.ini
        if get.path.find('.user.ini'):
            os.system("chattr -i '"+get.path+"'")
        try:
            if os.path.exists('data/recycle_bin.pl'):
                if self.Mv_Recycle_bin(get): return public.returnMsg(True,'FILE_MOVE_RECYCLE_BIN');
            os.remove(get.path)
            public.WriteLog('TYPE_FILE','FILE_DEL_SUCCESS',(get,path,))
            return public.returnMsg(True,'FILE_DEL_SUCCESS')
        except:
            return public.returnMsg(False,'FILE_DEL_ERR')
    
    #移动到回收站
    def Mv_Recycle_bin(self,get):
        rPath = '/www/Recycle_bin/'
        if not os.path.exists(rPath): os.system('mkdir -p ' + rPath);
        rFile = rPath + get.path.replace('/','_bt_') + '_t_' + str(time.time());
        try:
            import shutil
            shutil.move(get.path, rFile)
            public.WriteLog('TYPE_FILE','FILE_MOVE_RECYCLE_BIN',(get.path,))
            return True;
        except:
            public.WriteLog('TYPE_FILE','FILE_MOVE_RECYCLE_BIN_ERR',(get.path,))
            return False;
    
    #从回收站恢复
    def Re_Recycle_bin(self,get):
        rPath = '/www/Recycle_bin/'
        get.path = get.path.encode('utf-8');
        dFile = get.path.replace('_bt_','/').split('_t_')[0];
        get.path = rPath + get.path
        if dFile.find('BTDB_') != -1:
            import database;
            return database.database().RecycleDB(get.path);
        try:
            import shutil
            shutil.move(get.path, dFile)
            public.WriteLog('TYPE_FILE','FILE_RE_RECYCLE_BIN',(dFile,))
            return public.returnMsg(True,'FILE_RE_RECYCLE_BIN');
        except:
            public.WriteLog('TYPE_FILE','FILE_RE_RECYCLE_BIN_ERR',(dFile,))
            return public.returnMsg(False,'FILE_RE_RECYCLE_BIN_ERR');
    
    #获取回收站信息
    def Get_Recycle_bin(self,get):
        rPath = '/www/Recycle_bin/'
        if not os.path.exists(rPath): os.system('mkdir -p ' + rPath);
        data = {};
        data['dirs'] = [];
        data['files'] = [];
        data['status'] = os.path.exists('data/recycle_bin.pl');
        for file in os.listdir(rPath):
            try:
                tmp = {};
                fname = rPath + file;
                tmp1 = file.split('_bt_');
                tmp2 = tmp1[len(tmp1)-1].split('_t_');
                tmp['rname'] = file;
                tmp['dname'] = file.replace('_bt_','/').split('_t_')[0];
                tmp['name'] = tmp2[0];
                tmp['time'] = int(float(tmp2[1]));
                if os.path.islink(fname): 
                    filePath = os.readlink(fname);
                    link = ' -> ' + filePath;
                    if os.path.exists(filePath): 
                        tmp['size'] = os.path.getsize(filePath);
                    else:
                        tmp['size'] = 0;
                else:
                    tmp['size'] = os.path.getsize(fname);
                if os.path.isdir(fname):
                    data['dirs'].append(tmp);
                else:
                    data['files'].append(tmp);
            except:
                continue;
        return data;
    
    #彻底删除
    def Del_Recycle_bin(self,get):
        rPath = '/www/Recycle_bin/'
        get.path = get.path.encode('utf-8');
        dFile = get.path.split('_t_')[0];
        if dFile.find('BTDB_') != -1:
            import database;
            return database.database().DeleteTo(rPath+get.path);
        if not self.CheckDir(rPath + get.path):
            return public.returnMsg(False,'FILE_DANGER');
        os.system('chattr -R -i ' + rPath + get.path)
        if os.path.isdir(rPath + get.path):
            import shutil
            shutil.rmtree(rPath + get.path);
        else:
            os.remove(rPath + get.path);
        
        tfile = get.path.replace('_bt_','/').split('_t_')[0];
        public.WriteLog('TYPE_FILE','FILE_DEL_RECYCLE_BIN',(tfile,));
        return public.returnMsg(True,'FILE_DEL_RECYCLE_BIN',(tfile,));
    
    #清空回收站
    def Close_Recycle_bin(self,get):
        rPath = '/www/Recycle_bin/'
        os.system('chattr -R -i ' + rPath)
        import database,shutil;
        rlist = os.listdir(rPath)
        i = 0;
        l = len(rlist);
        for name in rlist:
            i += 1;
            path = rPath + name;
            public.writeSpeed(name,i,l);
            if name.find('BTDB_') != -1:
                database.database().DeleteTo(path);
                continue;
            if os.path.isdir(path):
                #os.system('rm -rf ' + path);
                shutil.rmtree(path);
            else:
                #os.system('rm -f ' + path);
                os.remove(path);
        public.writeSpeed(None,0,0);
        public.WriteLog('TYPE_FILE','FILE_CLOSE_RECYCLE_BIN');
        return public.returnMsg(True,'FILE_CLOSE_RECYCLE_BIN');
    
    #回收站开关
    def Recycle_bin(self,get):
        c = 'data/recycle_bin.pl'
        if os.path.exists(c):
            os.remove(c)
            public.WriteLog('TYPE_FILE','FILE_OFF_RECYCLE_BIN');
            return public.returnMsg(True,'FILE_OFF_RECYCLE_BIN');
        else:
            public.writeFile(c,'True');
            public.WriteLog('TYPE_FILE','FILE_ON_RECYCLE_BIN');
            return public.returnMsg(True,'FILE_ON_RECYCLE_BIN');
    
    #复制文件
    def CopyFile(self,get) :
        get.sfile = get.sfile.encode('utf-8');
        get.dfile = get.dfile.encode('utf-8');
        if not os.path.exists(get.sfile):
            return public.returnMsg(False,'FILE_NOT_EXISTS')
        
        if os.path.isdir(get.sfile):
            return self.CopyDir(get)
        
        import shutil
        try:
            shutil.copyfile(get.sfile, get.dfile)
            public.WriteLog('TYPE_FILE','FILE_COPY_SUCCESS',(get.sfile,get.dfile))
            self.SetFileAccept(get.dfile);
            return public.returnMsg(True,'FILE_COPY_SUCCESS')
        except:
            return public.returnMsg(False,'FILE_COPY_ERR')
    
    #复制文件夹
    def CopyDir(self,get):
        get.sfile = get.sfile.encode('utf-8');
        get.dfile = get.dfile.encode('utf-8');
        if not os.path.exists(get.sfile):
            return public.returnMsg(False,'DIR_NOT_EXISTS')
        
        if not self.CheckDir(get.dfile):
            return public.returnMsg(False,'FILE_DANGER');
        
        import shutil
        try:
            shutil.copytree(get.sfile, get.dfile)
            public.WriteLog('TYPE_FILE','DIR_COPY_SUCCESS',(get.sfile,get.dfile))
            self.SetFileAccept(get.dfile);
            return public.returnMsg(True,'DIR_COPY_SUCCESS')
        except:
            return public.returnMsg(False,'DIR_COPY_ERR')
        
    
    
    #移动文件或目录
    def MvFile(self,get) :
        get.sfile = get.sfile.encode('utf-8');
        get.dfile = get.dfile.encode('utf-8');
        if not os.path.exists(get.sfile):
            return public.returnMsg(False,'FILE_NOT_EXISTS')
        
        if os.path.exists(get.dfile):
            return public.returnMsg(False,'FILE_EXISTS')
        
        if not self.CheckDir(get.sfile):
            return public.returnMsg(False,'FILE_DANGER');
        
        import shutil
        try:
            shutil.move(get.sfile, get.dfile)
            public.WriteLog('TYPE_FILE','MOVE_SUCCESS',(get.sfile,get.dfile))
            return public.returnMsg(True,'MOVE_SUCCESS')
        except:
            return public.returnMsg(False,'MOVE_ERR')
    
        
    
    
    #获取文件内容
    def GetFileBody(self,get) :
        get.path = get.path.encode('utf-8');
        if not os.path.exists(get.path):
            if get.path.find('rewrite') == -1:
                return public.returnMsg(False,'FILE_NOT_EXISTS')
            public.writeFile(get.path,'');
        try:
            srcBody = public.readFile(get.path)
            
            data = {}
            if srcBody:
                import chardet
                char=chardet.detect(srcBody)
                data['encoding'] = char['encoding']
                if char['encoding'] == 'ascii':data['encoding'] = 'utf-8'
                data['data'] = srcBody.decode(char['encoding']).encode('utf-8')
            else:
                data['data'] = srcBody
                data['encoding'] = 'utf-8'
            
            data['status'] = True
            return data
        except:
            return public.returnMsg(False,'FILE_GET_ERR')
    
    
    #保存文件
    def SaveFileBody(self,get):
        get.path = get.path.encode('utf-8');
        if not os.path.exists(get.path):
            if get.path.find('.htaccess') == -1:
                return public.returnMsg(False,'FILE_NOT_EXISTS')
        
        try:
            isConf = -1
            if os.path.exists('/etc/init.d/nginx') or os.path.exists('/etc/init.d/httpd'):
                isConf = get.path.find('nginx');
                if isConf == -1: isConf = get.path.find('apache');
                if isConf == -1: isConf = get.path.find('rewrite');
                if isConf != -1:
                    os.system('\\cp -a '+get.path+' /tmp/backup.conf');
            
            data = get.data[0];
            
            if get.path.find('/www/server/cron') != -1:
                    try:
                        import crontab
                        data = crontab.crontab().CheckScript(data);
                    except:
                        pass
            
            if get.encoding == 'ascii':get.encoding = 'utf-8';
            public.writeFile(get.path,data.encode(get.encoding));
            
            if isConf != -1:
                isError = public.checkWebConfig();
                if isError != True:
                    os.system('\\cp -a /tmp/backup.conf '+get.path);
                    return public.returnMsg(False,'ERROR:<br><font style="color:red;">'+isError.replace("\n",'<br>')+'</font>');
                public.serviceReload();
                
            public.WriteLog('TYPE_FILE','FILE_SAVE_SUCCESS',(get.path,));
            return public.returnMsg(True,'FILE_SAVE_SUCCESS');
        except:
            return public.returnMsg(False,'FILE_SAVE_ERR');
        
    
    #文件压缩
    def Zip(self,get) :
        get.sfile = get.sfile.encode('utf-8');
        get.dfile = get.dfile.encode('utf-8');
        get.path = get.path.encode('utf-8');
        if get.sfile.find(',') == -1:
            if not os.path.exists(get.path+'/'+get.sfile): return public.returnMsg(False,'FILE_NOT_EXISTS');
        try:
            tmps = '/tmp/panelExec.log'
            if get.type == 'zip':
                os.system("cd '"+get.path+"' && zip '"+get.dfile+"' -r '"+get.sfile+"' > "+tmps+" 2>&1")
            else:
                sfiles = ''
                for sfile in get.sfile.split(','):
                    if not sfile: continue;
                    sfiles += " '" + sfile + "'";
                os.system("cd '" + get.path + "' && tar -zcvf '" + get.dfile + "' " + sfiles + " > " + tmps + " 2>&1");
            self.SetFileAccept(get.dfile);
            public.WriteLog("TYPE_FILE", 'ZIP_SUCCESS',(get.sfile,get.dfile));
            return public.returnMsg(True,'ZIP_SUCCESS')
        except:
            return public.returnMsg(False,'ZIP_ERR')
    
    
    #文件解压
    def UnZip(self,get):
        get.sfile = get.sfile.encode('utf-8');
        get.dfile = get.dfile.encode('utf-8');
        if not os.path.exists(get.sfile):
            return public.returnMsg(False,'FILE_NOT_EXISTS');
        
        if not hasattr(get,'password'): get.password = '';
        
        #try:
        if not hasattr(get,'coding'): get.coding = 'UTF-8';
        tmps = '/tmp/panelExec.log'
        if get.sfile[-4:] == '.zip':
            os.system("export LANG=\"zh_CN." + get.coding + "\" && unzip -P '"+get.password+"' -o '" + get.sfile + "' -d '" + get.dfile + "' > " + tmps + " 2>&1")
        elif get.sfile[-7:] == '.tar.gz' or get.sfile[-4:] == '.tgz':
            os.system("tar zxf '" + get.sfile + "' -C '" + get.dfile + "' > " + tmps + " 2>&1");
        else:
            os.system("gunzip -c " + get.sfile + " > " + get.sfile[:-3])
        if self.CheckDir(get.dfile):self.SetFileAccept(get.dfile);
        public.WriteLog("TYPE_FILE", 'UNZIP_SUCCESS',(get.sfile,get.dfile));
        return public.returnMsg(True,'UNZIP_SUCCESS');
        #except:
        #    return public.returnMsg(False,'文件解压失败!')
    
    
    #获取文件/目录 权限信息
    def GetFileAccess(self,get):
        get.filename = get.filename.encode('utf-8');
        data = {}
        try:
            import pwd
            stat = os.stat(get.filename)
            data['chmod'] = str(oct(stat.st_mode)[-3:])
            data['chown'] = pwd.getpwuid(stat.st_uid).pw_name
        except:
            data['chmod'] = 755
            data['chown'] = 'www'
        return data
    
    
    #设置文件权限和所有者
    def SetFileAccess(self,get,all = '-R'):
        get.filename = get.filename.encode('utf-8');
        try:
            if not self.CheckDir(get.filename): return public.returnMsg(False,'FILE_DANGER');
            if not os.path.exists(get.filename):
                return public.returnMsg(False,'FILE_NOT_EXISTS')
            os.system('chmod '+all+' '+get.access+" '"+get.filename+"'")
            os.system('chown '+all+' '+get.user+':'+get.user+" '"+get.filename+"'")
            public.WriteLog('TYPE_FILE','FILE_ACCESS_SUCCESS',(get.filename,get.access,get.user))
            return public.returnMsg(True,'SET_SUCCESS')
        except:
            return public.returnMsg(False,'SET_ERROR')

    def SetFileAccept(self,filename):
        os.system('chown -R www:www ' + filename)
        os.system('chmod -R 755 ' + filename)
    
    
    
    #取目录大小
    def GetDirSize(self,get):
        get.path = get.path.encode('utf-8');
        import web
        tmp = public.ExecShell('du -sbh '+ get.path)
        return tmp[0].split()[0]
    
    def CloseLogs(self,get):
        import web
        get.path = web.ctx.session.rootPath
        os.system('rm -f '+web.ctx.session.logsPath+'/*')
        if web.ctx.session.webserver == 'nginx':
            os.system('kill -USR1 `cat '+web.ctx.session.setupPath+'/nginx/logs/nginx.pid`');
        else:
            os.system('/etc/init.d/httpd reload');
        
        public.WriteLog('TYPE_FILE','SITE_LOG_CLOSE')
        get.path = web.ctx.session.logsPath
        return self.GetDirSize(get)
            
    #批量操作
    def SetBatchData(self,get):
        get.path = get.path.encode('utf-8');
        if get.type == '1' or get.type == '2':
            import web
            web.ctx.session.selected = get
            return public.returnMsg(True,'FILE_ALL_TIPS')
        elif get.type == '3':
            for key in get.data:
                try:
                    filename = get.path+'/'+key.encode('utf-8');
                    if not self.CheckDir(filename): return public.returnMsg(False,'FILE_DANGER');
                    os.system('chmod -R '+get.access+" '"+filename+"'")
                    os.system('chown -R '+get.user+':'+get.user+" '"+filename+"'")
                except:
                    continue;
            public.WriteLog('TYPE_FILE','FILE_ALL_ACCESS')
            return public.returnMsg(True,'FILE_ALL_ACCESS')
        else:
            import shutil
            isRecyle = os.path.exists('data/recycle_bin.pl')
            path = get.path
            l = len(get.data);
            i = 0;
            for key in get.data:
                try:
                    filename = path + '/'+key.encode('utf-8');
                    get.path = filename;
                    if not os.path.exists(filename): continue
                    i += 1;
                    public.writeSpeed(key,i,l);
                    if os.path.isdir(filename):
                        if not self.CheckDir(filename): return public.returnMsg(False,'FILE_DANGER');
                        if isRecyle:
                            self.Mv_Recycle_bin(get)
                        else:
                            shutil.rmtree(filename)
                    else:
                        if key == '.user.ini': os.system('chattr -i ' + filename);
                        if isRecyle:
                            
                            self.Mv_Recycle_bin(get)
                        else:
                            os.remove(filename)
                except:
                    continue;
                public.writeSpeed(None,0,0);
            public.WriteLog('TYPE_FILE','FILE_ALL_DEL')
            return public.returnMsg(True,'FILE_ALL_DEL')
    
    
    #批量粘贴
    def BatchPaste(self,get):
        import shutil,web
        get.path = get.path.encode('utf-8');
        if not self.CheckDir(get.path): return public.returnMsg(False,'FILE_DANGER');
        i = 0;
        l = len(web.ctx.session.selected.data);
        if get.type == '1':
            for key in web.ctx.session.selected.data:
                i += 1
                public.writeSpeed(key,i,l);
                try:
                    sfile = web.ctx.session.selected.path + '/' + key.encode('utf-8')
                    dfile = get.path + '/' + key.encode('utf-8')
                    if os.path.isdir(sfile):
                        shutil.copytree(sfile,dfile)
                    else:
                        shutil.copyfile(sfile,dfile)
                except:
                    continue;
            public.WriteLog('TYPE_FILE','FILE_ALL_COPY',(web.ctx.session.selected.path,get.path))
        else:
            for key in web.ctx.session.selected.data:
                try:
                    i += 1
                    public.writeSpeed(key,i,l);
                    sfile = web.ctx.session.selected.path + '/' + key.encode('utf-8')
                    dfile = get.path + '/' + key.encode('utf-8')
                    shutil.move(sfile,dfile)
                except:
                    continue;
            public.WriteLog('TYPE_FILE','FILE_ALL_MOTE',(web.ctx.session.selected.path,get.path))
        public.writeSpeed(None,0,0);
        errorCount = len(web.ctx.session.selected.data) - i
        del(web.ctx.session.selected)
        return public.returnMsg(True,'FILE_ALL',(str(i),str(errorCount)));
    
    #下载文件
    def DownloadFile(self,get):
        get.path = get.path.encode('utf-8');
        import db,time
        isTask = '/tmp/panelTask.pl'
        execstr = get.url +'|bt|'+get.path+'/'+get.filename
        sql = db.Sql()
        sql.table('tasks').add('name,type,status,addtime,execstr',('下载文件['+get.filename+']','download','0',time.strftime('%Y-%m-%d %H:%M:%S'),execstr))
        public.writeFile(isTask,'True')
        self.SetFileAccept(get.path+'/'+get.filename);
        public.WriteLog('TYPE_FILE','FILE_DOWNLOAD',(get.url , get.path));
        return public.returnMsg(True,'FILE_DOANLOAD')
    
    #添加安装任务
    def InstallSoft(self,get):
        import db,time,web
        path = web.ctx.session.setupPath + '/php'
        if not os.path.exists(path): os.system("mkdir -p " + path);
        if web.ctx.session.server_os['x'] != 'RHEL': get.type = '3'
        apacheVersion='false';
        if web.ctx.session.webserver == 'apache':
            apacheVersion = public.readFile(web.ctx.session.setupPath+'/apache/version.pl');
        public.writeFile('/var/bt_apacheVersion.pl',apacheVersion)
        public.writeFile('/var/bt_setupPath.conf',web.ctx.session.rootPath)
        isTask = '/tmp/panelTask.pl'
        execstr = "cd " + web.ctx.session.setupPath + "/panel/install && /bin/bash install_soft.sh " + get.type + " install " + get.name + " "+ get.version;
        sql = db.Sql()
        if hasattr(get,'id'):
            id = get.id;
        else:
            id = None;
        sql.table('tasks').add('id,name,type,status,addtime,execstr',(None,'安装['+get.name+'-'+get.version+']','execshell','0',time.strftime('%Y-%m-%d %H:%M:%S'),execstr))
        public.writeFile(isTask,'True')
        public.WriteLog('TYPE_SETUP','PLUGIN_ADD',(get.name,get.version));
        time.sleep(0.1);
        return public.returnMsg(True,'PLUGIN_ADD');
    
    #删除任务队列
    def RemoveTask(self,get):
        try:
            name = public.M('tasks').where('id=?',(get.id,)).getField('name');
            status = public.M('tasks').where('id=?',(get.id,)).getField('status');
            public.M('tasks').delete(get.id);
            if status == '-1':
                os.system("kill `ps -ef |grep 'python panelSafe.pyc'|grep -v grep|grep -v panelExec|awk '{print $2}'`");
                os.system("kill `ps -ef |grep 'install_soft.sh'|grep -v grep|grep -v panelExec|awk '{print $2}'`");
                os.system("kill `ps aux | grep 'python task.pyc$'|awk '{print $2}'`");
                os.system('''
pids=`ps aux | grep 'sh'|grep -v grep|grep install|awk '{print $2}'`
arr=($pids)

for p in ${arr[@]}
do
    kill -9 $p
done
            ''');
            
                os.system('rm -f ' + name.replace('扫描目录[','').replace(']','') + '/scan.pl');
                isTask = '/tmp/panelTask.pl';
                public.writeFile(isTask,'True');
                os.system('/etc/init.d/bt start');
        except:
            os.system('/etc/init.d/bt start');
        return public.returnMsg(True,'PLUGIN_DEL');
    
    #重新激活任务
    def ActionTask(self,get):
        isTask = '/tmp/panelTask.pl'
        public.writeFile(isTask,'True');
        return public.returnMsg(True,'PLUGIN_ACTION');
        
    
    #卸载软件
    def UninstallSoft(self,get):
        import web
        public.writeFile('/var/bt_setupPath.conf',web.ctx.session.rootPath)
        get.type = '0'
        if web.ctx.session.server_os['x'] != 'RHEL': get.type = '3'
        execstr = "cd " + web.ctx.session.setupPath + "/panel/install && /bin/bash install_soft.sh "+get.type+" uninstall " + get.name.lower() + " "+ get.version.replace('.','');
        os.system(execstr);
        public.WriteLog('TYPE_SETUP','PLUGIN_UNINSTALL',(get.name,get.version));
        return public.returnMsg(True,"PLUGIN_UNINSTALL");
        
    
    #取任务队列进度
    def GetTaskSpeed(self,get):
        tempFile = '/tmp/panelExec.log'
        freshFile = '/tmp/panelFresh'
        import db
        find = db.Sql().table('tasks').where('status=? OR status=?',('-1','0')).field('id,type,name,execstr').find()
        if not len(find): return public.returnMsg(False,'当前没有任务队列在执行-2!')
        isTask = '/tmp/panelTask.pl'
        public.writeFile(isTask,'True');
        echoMsg = {}
        echoMsg['name'] = find['name']
        echoMsg['execstr'] = find['execstr']
        if find['type'] == 'download':
            import json
            try:
                tmp = public.readFile(tempFile)
                if len(tmp) < 10:
                    return public.returnMsg(False,'当前没有任务队列在执行-3!')
                echoMsg['msg'] = json.loads(tmp)
                echoMsg['isDownload'] = True
            except:
                db.Sql().table('tasks').where("id=?",(find['id'],)).save('status',('0',))
                return public.returnMsg(False,'当前没有任务队列在执行-4!')
        else:
            echoMsg['msg'] = self.GetLastLine(tempFile,20)
            echoMsg['isDownload'] = False
        
        echoMsg['task'] = public.M('tasks').where("status!=?",('1',)).field('id,status,name,type').order("id asc").select()
        return echoMsg
                 
    #读文件指定倒数行数
    def GetLastLine(self,inputfile,lineNum):
        try:
            fp = open(inputfile, 'r')
            lastLine = ""
            
            lines =  fp.readlines()
            count = len(lines)
            if count>lineNum:
                num=lineNum
            else:
                num=count
            i=1;
            lastre = []
            for i in range(1,(num+1)):
                if lines :
                    n = -i
                    lastLine = lines[n].strip()
                    fp.close()
                    lastre.append(lastLine)
            
            result = ''
            lineNum -= 1
            while lineNum > 0:
                result += lastre[lineNum]+"\n"
                lineNum -= 1
                
            return result
        except:
            return public.getMsg('TASK_SLEEP');
        
    
    #执行SHELL命令
    def ExecShell(self,get):
        disabled = ['vi','vim','top','passwd','su']
        get.shell = get.shell.strip()
        tmp = get.shell.split(' ');
        if tmp[0] in disabled: return public.returnMsg(False,'FILE_SHELL_ERR',(tmp[0],));
        shellStr = '''#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
cd %s
%s
''' % (get.path,get.shell)
        public.writeFile('/tmp/panelShell.sh',shellStr);
        os.system('nohup bash /tmp/panelShell.sh > /tmp/panelShell.pl 2>&1 &');
        return public.returnMsg(True,'FILE_SHELL_EXEC');
    
    #取SHELL执行结果
    def GetExecShellMsg(self,get):
        fileName = '/tmp/panelShell.pl';
        if not os.path.exists(fileName): return 'FILE_SHELL_EMPTY';
        return public.readFile('/tmp/panelShell.pl');
    
    #文件搜索
    def GetSearch(self,get):
        if not os.path.exists(get.path): return public.returnMsg(False,'DIR_NOT_EXISTS');
        return public.ExecShell("find "+get.path+" -name '*"+get.search+"*'");
        
        

