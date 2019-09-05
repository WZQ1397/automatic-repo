import datetime,os
class BatchDirDeploy:
    def __init__(self,num:int,symbol="-"):
        self.num=num
        self.PRE_LIST=[]
        self.SUF_LIST = []
        self.symbol=symbol

    def batchnum(self,level=2) -> int:
        return self.num,level

    def ChkName(self,name) -> str:
        '''
        Check whether name value is empty
        :param name is must
        :return:
        '''
        return self.symbol if len(name) else ""

    def prefix(self, PREFIX_NAME) -> list :
        '''
        CREATE FILE NAME LIKE :  1-xxx,3-xxx if you input the prefix name
        :param PREFIX_NAME: default zach
        :return:
        '''
        if PREFIX_NAME[:1].islower():
           PREFIX_NAME = PREFIX_NAME.capitalize()
        for ind in range(self.num):
            self.PRE_LIST.append(PREFIX_NAME+self.ChkName(PREFIX_NAME)+str(ind))
        return self.PRE_LIST

    def suffix(self,SUFFIX_NAME) -> list:
        '''
        CREATE FILE NAME LIKE :  Xxx-1,Xxx-3 if you input the suffix name
        :param SUFFIX_NAME: default -> none
        :return:
        '''
        if len(self.PRE_LIST):
            for ind in range(self.num):
                self.SUF_LIST.append(self.PRE_LIST[ind]+self.ChkName(SUFFIX_NAME)+SUFFIX_NAME)
        else:
            for ind in range(self.num):
                self.SUF_LIST.append(str(ind)+self.ChkName(SUFFIX_NAME)+SUFFIX_NAME)
        return self.SUF_LIST

    def usedatetime(self,DATE_FORMAT=str(datetime.date.today())) -> list:
        LST=[]

        if len(self.PRE_LIST):
            for ind in range(self.num):
                #print(DATE_FORMAT)
                LST.append(self.SUF_LIST[ind]+"-"+DATE_FORMAT)
        else:
            for ind in range(self.num):
                LST.append(str(ind)+"-"+DATE_FORMAT)
        return LST

class CreateDir:
    def __init__(self,FILE_ARRAY):
        self.FILE_ARRAY=FILE_ARRAY

    def Create(self):
        for lst in self.FILE_ARRAY:
            os.mkdir(lst)
        os.listdir()