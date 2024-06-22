import pymysql

from configs.config import Config


class SQLHandler(object):

    def __init__(self):
        self.config = Config()
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.config.DB_HOST,
                                    user=self.config.DB_USER,
                                    password=self.config.DB_PASSWORD,
                                    database=self.config.DB_NAME)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def execute(self, sql, params=None, autocommit=True) -> tuple:
        try:
            self.cursor.execute(sql, params)
            if autocommit:
                self.commit()
            return True, "Success"
        except Exception as e:
            self.conn.rollback()
            return False, f"{e}"

    def commit(self):
        self.conn.commit()

    def query(self, sql, params=None) -> tuple:
        try:
            self.cursor.execute(sql, params)
            query_result = self.cursor.fetchall()
            self.commit()
            return True, query_result
        except Exception as e:
            self.conn.rollback()
            return False, f"{e}"