import pymysql.cursors

class BaseModel():
    def __init__(self, config):
        self.host = config['host']
        self.user = config['user']
        self.db = config['db']
        self.charset = config['charset']

    def get_connection(self):
        '''
        MySQLデータベースに接続
        '''
        conn = pymysql.connect(host=self.host,
                        user=self.user,
                        db=self.db,
                        charset=self.charset,
                        cursorclass=pymysql.cursors.DictCursor)
        return conn
    
    def insert_single_record(self, table, colmun, values):
        '''
        シングルレコードのINSERT \n
        table: テーブル名  values: tuple \n
        return -> 最後に追加したレコードのid
        '''
        conn = self.get_connection()
        wildcard = "%s,"*len(values)
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO " + table + " (" + colmun + ") VALUES (%s, %s)"
                print(sql)
                cursor.execute(sql, values)
                lastid = cursor.lastrowid
        except Exception as e:
            return {"error":e}
        conn.commit()
        conn.close()
        return lastid
    
    def bulk_insert_records(self, table, colmun, values):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO " + table + " (" + colmun + ") VALUES (%s, %s, %s)"
                cursor.executemany(sql, values)
        except Exception as e:
            print(e)
            return {"error":e}
        conn.commit()
        conn.close()

    def select(self, table, colmun, option=''):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT " + colmun + " FROM " + table + option
                print(sql)
                cursor.execute(sql)
                result = cursor.fetchall()
        finally: conn.close()
        return result
    
    def select_by_id(self, table, colmun, where):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT " + colmun + " FROM " + table + where
                print(sql)
                cursor.execute(sql)
                result = cursor.fetchall()
        finally: conn.close()
        return result
    
    def delete(self, table , option=''):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM " + table + option
                cursor.execute(sql)
        except Exception as e:
            return {"error":e}
        conn.commit()
        conn.close()
        return