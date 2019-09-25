import datetime,os
from re import search
from abc import abstractmethod
class BatchDirDeploy:
    def __init__(self,num:int,symbol="-"):
        '''
         private property 外部无法直接访问
        :param num:
        :param symbol:
        '''

        self.__num=num
        self.__PRE_LIST=[]
        self.__SUF_LIST = []
        self.__symbol=symbol

    def ChkName(self,name) -> str:
        '''
        Check whether name value is empty
        :param name is must
        :return:
        '''
        return self.__symbol if len(name) else ""

    def prefix(self, PREFIX_NAME) -> list :
        '''
        CREATE FILE NAME LIKE :  1-xxx,3-xxx if you input the prefix name
        :param PREFIX_NAME: default zach
        :return:
        '''
        if PREFIX_NAME[:1].islower():
           PREFIX_NAME = PREFIX_NAME.capitalize()
        for ind in range(self.__num):
            self.__PRE_LIST.append(PREFIX_NAME+self.ChkName(PREFIX_NAME)+str(ind))
        return self.__PRE_LIST

    def suffix(self,SUFFIX_NAME) -> list:
        '''
        CREATE FILE NAME LIKE :  Xxx-1,Xxx-3 if you input the suffix name
        :param SUFFIX_NAME: default -> none
        :return:
        '''
        if len(self.__PRE_LIST):
            for ind in range(self.__num):
                self.__SUF_LIST.append(self.__PRE_LIST[ind]+self.ChkName(SUFFIX_NAME)+SUFFIX_NAME)
        else:
            for ind in range(self.__num):
                self.__SUF_LIST.append(str(ind)+self.ChkName(SUFFIX_NAME)+SUFFIX_NAME)
        return self.__SUF_LIST

    def usedatetime(self,DATE_FORMAT=str(datetime.date.today())) -> list:
        LST=[]

        if len(self.__PRE_LIST):
            for ind in range(self.__num):
                #print(DATE_FORMAT)
                LST.append(self.__SUF_LIST[ind]+"-"+DATE_FORMAT)
        else:
            for ind in range(self.__num):
                LST.append(str(ind)+"-"+DATE_FORMAT)
        return LST

class ChkSyntax:
    '''
    这是父类
    '''
    def __init__(self,content):
        self.content=content

    @abstractmethod
    def chk_format(self):
        '''
        abstract method need to reload in sub class
        :return:
        '''
        pass

    def __bool__(self):
        return type(self.chk_format) is int

class IsVaildDate(ChkSyntax):
    def __init__(self,content):
        super().__init__(content)
        self.MonthList=[mon for mon in range(1,13)]
        self.DayList=[31,28,31,30,31,30,31,31,30,31,30,31]
        self.DateDict=dict(zip(self.MonthList,self.DayList))

    @property
    def chk_format(self):
        str=self.content
        DATE_REGEX=r'(\d{4})-(\d{2})-(\d{2})'
        content=search(DATE_REGEX,str.strip())
        # content=match(DATE_REGEX,str.strip())

       # print(self.DateDict)
       # print(bool(content))
        if content:
            Year=int(content.group(1))
            Month=int(content.group(2))
            Day=int(content.group(3))
            if Year > 1970 and Month in self.MonthList:
                return self.MonthList.index(Month)

    # def __bool__(self):
    #     return type(self.chk_format) is int

class IsVaildName(ChkSyntax):

    @property
    def chk_format(self):
        str=self.content
        DATE_REGEX=r'(\w+)'
        content=search(DATE_REGEX,str.strip())
        return content.group(1)==str

    def __bool__(self):
        '''
        rewrite methed
        :return: bool
        '''
        return self.chk_format

class CreateDir:
    def __init__(self,FILE_ARRAY):
        self.FILE_ARRAY=FILE_ARRAY

    def Create(self):
        for lst in self.FILE_ARRAY:
            os.mkdir(lst)
        os.listdir()