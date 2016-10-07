import pymysql

class DatabaseConnector:
    def __init__(self):
        self.conn =pymysql.connect(host='127.0.0.1',user='root',password="dlawnstn123",db='wiki')
        self.cur=self.conn.cursor(pymysql.cursors.DictCursor)
    def query_insert(self,q):
        print(q)
        try:
            self.cur.execute(q)
            self.conn.commit()
            return 1
        except:
            return 0
        return
    def query_select(self,q):
        print(q);
        result={};
        result['NUM']=self.cur.execute(q);
        result['ROW']=self.cur.fetchone();
        result['ALL']=self.cur.fetchall();
        return result
    def commit(self):
        return self.conn.commit()
    def __del__(self):
        self.cur.close()
        self.conn.close()

