import pymysql

class DatabaseConnector:
    def __init__(self):
        self.conn =pymysql.connect(host='127.0.0.1',user='root',password="dlawnstn123",db='wiki')
        self.cur=self.conn.cursor(pymysql.cursors.DictCursor)
    def query(self,q):
        print(q)
        return self.cur.execute(q)
    def __del__(self):
        self.cur.close()
        self.conn.close()

