from mongo import pymongoconn

dbconn = pymongoconn.DBConn()
conn = None
#TODO TABLE_NAME
zach = None

FILE_PATH = 'E:\\python\\useragent.bin'

def process():
    #TODO 建立连接
    dbconn.connect()
    global conn
    conn = dbconn.getConn()

def insertValues():
    with open(FILE_PATH) as f:
        for value in f.readline():
            #FIXME
            print(type(eval(value)))
            #zach.insert()

def createTable():
    '''创建库和表'''
    global zach
    zach = conn.zach.bulktest

def printResult(rows):
    for row in rows:
        for key in row.keys():#遍历字典
            print(row[key],) #加, 不换行打印
        print('')

def queryData():
    #TODO 查询全部数据
    rows = zach.find()
    printResult(rows)

if __name__ == '__main__':
    process()
    createTable()
    insertValues()
    queryData()