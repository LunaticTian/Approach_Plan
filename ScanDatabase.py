import pymysql.cursors
from datetime import datetime, timedelta
import time
# 获取数据库命令对象

class Scanf():
    connect = None
    cursor = None
    def __init__(self,connect):
        self.connect = connect
        self.cursor = connect.cursor()
        while 1:
            time.sleep(2880)
            self.openDatabase()

    def ScanfTime(self):
        now = datetime.now()
        releaseTime = now - timedelta(days=int(15))
        releaseTime = str(releaseTime)[0:10]
        # 获取游标
        sql = 'UPDATE work SET vk = 0 WHERE time < ' + releaseTime
        self.cursor.execute(sql)
        self.connect.commit()

