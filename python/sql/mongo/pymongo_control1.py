from mongo import pymongoconn

dbconn = pymongoconn.DBConn()
conn = None
#TODO TABLE_NAME
zach = None

def process():
    #TODO 建立连接
    dbconn.connect()
    global conn
    conn = dbconn.getConn()

    #列出server_info信息
    #print(conn.server_info())

    #TODO 列出全部数据库
    databases = conn.database_names()
    print(databases)

    #删除库和表
    dropTable()
    #添加数据库zach及表(collections)users
    createTable()
    #插入数据
    insertDatas()
    #更新数据
    updateData()
    #查询数据
    queryData()
    #删除数据
    #deleteData()

    #释放连接
    #dbconn.close()

def insertDatas():
    datas=[{"name":"steven1","realname":"测试1","age":25},
           {"name":"steven2","realname":"测试2","age":26},
           {"name":"steven1","realname":"测试3","age":23}]
    zach.insert(datas)

def updateData():
    '''只修改最后一条匹配到的数据
           第3个参数设置为True,没找到该数据就添加一条
           第4个参数设置为True,有多条记录就不更新
    '''
    zach.update({'name':'steven1'},{'$set':{'realname':'测试1修改'}}, False,False)

def deleteData():
    zach.remove({'name':'steven1'})

def queryData():
    #TODO 查询全部数据
    rows = zach.find()
    #printResult(rows)
    #TODO 查询一个数据
    #print (zach.find_one())
    #TODO 带条件查询
    #printResult(zach.find({'name':'steven2'}))
    printResult(zach.find({'age':{'$gt':25}}))

def createTable():
    '''创建库和表'''
    global zach
    zach = conn.zach.test1

def dropTable():
    '''删除表'''
    global conn
    conn.drop_database("zach")

def printResult(rows):
    for row in rows:
        for key in row.keys():#遍历字典
            print(row[key],) #加, 不换行打印
        print('')

if __name__ == '__main__':
    process()