import pymongo
class DBConn:
    conn = None
    servers = "mongodb://172.16.10.120:27017"

    def connect(self):
        self.conn = pymongo.MongoClient(self.servers)

    def close(self):
        return self.conn.disconnect()

    def getConn(self):
        return self.conn