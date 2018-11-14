#coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2016 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <2879625666@qq.com>
# +-------------------------------------------------------------------
import math,string,public

class Page():
    #--------------------------
    # 分页类 - JS回调版
    #--------------------------
    __PREV          =   '上一页'
    __NEXT          =   '下一页'
    __START         =   '首页'
    __END           =   '尾页'
    __COUNT_START   =   '共'
    __COUNT_END     =   '条数据'
    __FO            =   '从'
    __LINE          =   '条'
    __LIST_NUM      =  4
    SHIFT         =  None           #偏移量
    ROW           =  None           #每页行数
    __C_PAGE        =  None           #当前页
    __COUNT_PAGE    =  None           #总页数
    __COUNT_ROW     =  None           #总行数
    __URI           =  None           #URI
    __RTURN_JS      =  False          #是否返回JS回调
    __START_NUM     =  None           #起始行
    __END_NUM       =  None           #结束行
    
    def __init__(self):
        tmp = public.getMsg('PAGE');
        if tmp:
            self.__PREV         = tmp['PREV'];
            self.__NEXT         = tmp['NEXT'];
            self.__START        = tmp['START'];
            self.__END          = tmp['END'];
            self.__COUNT_START  = tmp['COUNT_START'];
            self.__COUNT_END    = tmp['COUNT_END'];
            self.__FO           = tmp['FO'];
            self.__LINE         = tmp['LINE'];
    
    def GetPage(self,pageInfo,limit = '1,2,3,4,5,6,7,8'):
        # 取分页信息
        # @param pageInfo 传入分页参数字典
        # @param limit 返回系列
        self.__RTURN_JS    = pageInfo['return_js']
        self.__COUNT_ROW   = pageInfo['count']
        self.ROW         = pageInfo['row']
        self.__C_PAGE      = self.__GetCpage(pageInfo['p'])
        self.__START_NUM   = self.__StartRow()
        self.__END_NUM     = self.__EndRow()
        self.__COUNT_PAGE  = self.__GetCountPage()
        self.__URI         = self.__SetUri(pageInfo['uri'])
        self.SHIFT       = self.__START_NUM - 1
        
        keys = limit.split(',')
        
        pages = {}
        #起始页
        pages['1'] = self.__GetStart()
        #上一页
        pages['2'] = self.__GetPrev()
        #分页
        pages['3'] = self.__GetPages()
        #下一页
        pages['4'] = self.__GetNext()
        #尾页
        pages['5'] = self.__GetEnd()
        
        #当前显示页与总页数
        pages['6'] = "<span class='Pnumber'>" + bytes(self.__C_PAGE) + "/" + bytes(self.__COUNT_PAGE) + "</span>"
        #本页显示开始与结束行
        pages['7'] = "<span class='Pline'>" + self.__FO + bytes(self.__START_NUM) + "-" + bytes(self.__END_NUM) + self.__LINE + "</span>"
        #行数
        pages['8'] = "<span class='Pcount'>" + self.__COUNT_START + bytes(self.__COUNT_ROW) + self.__COUNT_END + "</span>"
        
        #构造返回数据
        retuls = '<div>';
        for value in keys:
            retuls += pages[value]
        retuls +='</div>';
        
        #返回分页数据
        return retuls;
            
    def __GetEnd(self):
        #构造尾页
        endStr = ""
        if self.__C_PAGE >= self.__COUNT_PAGE:
            endStr = '';
        else:
            if self.__RTURN_JS == "":
                endStr = "<a class='Pend' href='" + self.__URI + "p=" + bytes(self.__COUNT_PAGE) + "'>" + self.__END + "</a>"
            else:
                endStr = "<a class='Pend' onclick='" + self.__RTURN_JS + "(" + bytes(self.__COUNT_PAGE) + ")'>" + self.__END + "</a>"
        return endStr
    
    def __GetNext(self):
        #构造下一页
        nextStr = ""
        if self.__C_PAGE >= self.__COUNT_PAGE:
            nextStr = '';
        else:
            if self.__RTURN_JS == "":
                nextStr = "<a class='Pnext' href='" + self.__URI + "p=" + bytes(self.__C_PAGE + 1) + "'>" + self.__NEXT + "</a>"
            else:    
                nextStr = "<a class='Pnext' onclick='" + self.__RTURN_JS + "(" + bytes(self.__C_PAGE + 1) + ")'>" + self.__NEXT + "</a>"
        
        return nextStr
    
    def __GetPages(self):
        #构造分页
        pages = ''
        num   = 0
        #当前页之前
        if (self.__COUNT_PAGE - self.__C_PAGE) < self.__LIST_NUM:
            num = self.__LIST_NUM + (self.__LIST_NUM - (self.__COUNT_PAGE - self.__C_PAGE));
        else:
            num = self.__LIST_NUM
        n = 0
        for i in range(num):
            n = num - i
            page = self.__C_PAGE - n;
            if page > 0:
                if self.__RTURN_JS == "":
                    pages += "<a class='Pnum' href='" + self.__URI + "p=" + bytes(page) + "'>" + bytes(page) + "</a>"
                else:
                    pages += "<a class='Pnum' onclick='" + self.__RTURN_JS + "(" + bytes(page) + ")'>" + bytes(page) + "</a>"
            
        #当前页
        if self.__C_PAGE > 0:
                pages += "<span class='Pcurrent'>" + bytes(self.__C_PAGE) + "</span>"
        
        #当前页之后
        if self.__C_PAGE <= self.__LIST_NUM:
            num = self.__LIST_NUM + (self.__LIST_NUM - self.__C_PAGE) + 1
        else:
            num = self.__LIST_NUM;
        for i in range(num):
            if i == 0:
                continue
            page = self.__C_PAGE + i;
            if page > self.__COUNT_PAGE:
                break;
            if self.__RTURN_JS == "":
                pages += "<a class='Pnum' href='" + self.__URI + "p=" + bytes(page) + "'>" + bytes(page) + "</a>"
            else:    
                pages += "<a class='Pnum' onclick='" + self.__RTURN_JS + "(" + bytes(page) + ")'>" + bytes(page) + "</a>"
                
        return pages;
    
    def __GetPrev(self):
        #构造上一页
        startStr = ''
        if self.__C_PAGE == 1:
            startStr = '';
        else:
            if self.__RTURN_JS == "":
                startStr = "<a class='Ppren' href='" + self.__URI + "p=" + bytes(self.__C_PAGE - 1) + "'>" + self.__PREV + "</a>"
            else:    
                startStr = "<a class='Ppren' onclick='" + self.__RTURN_JS + "(" + bytes(self.__C_PAGE - 1) + ")'>" + self.__PREV + "</a>"
        return startStr
    
    def __GetStart(self):
        #构造起始分页
        startStr = ''
        if self.__C_PAGE == 1:
            startStr = '';
        else:
            if self.__RTURN_JS == "":
                startStr = "<a class='Pstart' href='" + self.__URI + "p=1'>" + self.__START + "</a>"
            else:
                startStr = "<a class='Pstart' onclick='" + self.__RTURN_JS + "(1)'>" + self.__START + "</a>"
        return startStr;
    
    def __GetCpage(self,p):
        #取当前页
        if p:
            return p
        return 1
        
    def __StartRow(self):
        #从多少行开始
        return (self.__C_PAGE - 1) * self.ROW + 1
    
    def __EndRow(self):
        #从多少行结束
        if self.ROW > self.__COUNT_ROW:
            return self.__COUNT_ROW
        return self.__C_PAGE * self.ROW
    
    def __GetCountPage(self):
        #取总页数
        return int(math.ceil(self.__COUNT_ROW / float(self.ROW)))
    
    def __SetUri(self,input):
        #构造URI
        uri = '?'
        for key in input:
            if key == 'p':
                continue
            uri += key+'='+input[key]+'&'
        return str(uri)
