import pymysql

from configs.config import Config


class BaseTable(object):

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

    def execute(self, sql, params=None):
        if not self.conn or not self.cursor:
            self.connect()
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            print(f"Database Error: {e}")
            self.conn.rollback()
