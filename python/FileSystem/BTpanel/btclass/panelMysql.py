#coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2016 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <2879625666@qq.com>
# +-------------------------------------------------------------------

import re,os

class panelMysql:
    __DB_PASS = None
    __DB_USER = 'root'
    __DB_PORT = 3306
    __DB_HOST = '127.0.0.1'
    __DB_CONN = None
    __DB_CUR  = None
    __DB_ERR  = None
    __DB_HOST_CONF = 'data/mysqlHost.pl';
    #连接MYSQL数据库
    def __Conn(self):
        try:
            import public
            try:
                import MySQLdb
            except Exception,ex:
                self.__DB_ERR = ex
                return False;
            try:
                myconf = public.readFile('/etc/my.cnf');
                rep = "port\s*=\s*([0-9]+)"
                self.__DB_PORT = int(re.search(rep,myconf).groups()[0]);
            except:
                self.__DB_PORT = 3306;
            self.__DB_PASS = public.M('config').where('id=?',(1,)).getField('mysql_root');
            try:
                if os.path.exists(self.__DB_HOST_CONF): self.__DB_HOST = public.readFile(self.__DB_HOST_CONF);
                self.__DB_CONN = MySQLdb.connect(host = self.__DB_HOST,user = self.__DB_USER,passwd = self.__DB_PASS,port = self.__DB_PORT,charset="utf8",connect_timeout=1)
            except MySQLdb.Error,e:
                if e[0] != 2003: 
                    self.__DB_ERR = e
                    return False
                if self.__DB_HOST == 'localhost':
                    self.__DB_HOST = '127.0.0.1';
                else:
                    self.__DB_HOST = 'localhost';
                public.writeFile(self.__DB_HOST_CONF,self.__DB_HOST);
                self.__DB_CONN = MySQLdb.connect(host = self.__DB_HOST,user = self.__DB_USER,passwd = self.__DB_PASS,port = self.__DB_PORT,charset="utf8",connect_timeout=1)
            self.__DB_CUR  = self.__DB_CONN.cursor()
            return True
        except MySQLdb.Error,e:
            self.__DB_ERR = e
            return False
          
    def execute(self,sql):
        #执行SQL语句返回受影响行
        if not self.__Conn(): return self.__DB_ERR
        try:
            result = self.__DB_CUR.execute(sql)
            self.__DB_CONN.commit()
            self.__Close()
            return result
        except Exception,ex:
            return ex
    
    
    def query(self,sql):
        #执行SQL语句返回数据集
        if not self.__Conn(): return self.__DB_ERR
        try:
            self.__DB_CUR.execute(sql)
            result = self.__DB_CUR.fetchall()
            #将元组转换成列表
            data = map(list,result)
            self.__Close()
            return data
        except Exception,ex:
            return ex
        
     
    #关闭连接        
    def __Close(self):
        self.__DB_CUR.close()
        self.__DB_CONN.close()