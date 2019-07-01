import pymysql.cursors

# 获取数据库命令对象
def openDatabase():
    # 打开数据库连接
    connect = pymysql.Connect(
        host='',
        port=3306,
        user='',
        passwd='',
        db='Approach_Plan',
        charset='utf8'
    )
    # 获取游标
    cursor = connect.cursor()
    return cursor

class workData:
    workUrl = ''
    # 职位描述
    description = ''
    # 职位诱惑
    Lure = ''
    # 公司名称
    company = ''
    # 发布时间
    releaseTime = ''
    # 关键词
    key = ''
    # 工作性质
    nature = ''
    # 学历
    Education = ''
    # 经验
    experience = ''
    # 地点
    local = ''
    # 职位
    position = ''
    # 薪水
    salary = ''
    # 数据库连接
    cursor = None
    # 是否加入
    Tos  = 3
    # 不同时间ID保存
    id = None

    connect = None
    def __init__(self,workUrl,description,Lure,company,releaseTime,key,nature,Education,experience,local,position,salary,cursor,connect):
        self.workUrl = workUrl
        self.description = description
        self.Lure = Lure
        self.company = company
        self.releaseTime = releaseTime
        self.key = key
        self.nature = nature
        self.Education = Education
        self.experience = experience
        self.local = local
        self.position = position
        self.salary = salary
        self.cursor = cursor
        self.connect = connect


    def addData(self):
        # 完全相同
        if self.Tos == 3:
            pass
        # 时间不同，进行更新
        elif self.Tos == 2:
            sql = 'UPDATE work SET time = '+ self.releaseTime +', vk = 1 '+  'WHERE id = '+ id
            self.cursor.execute(sql)
            self.connect.commit()
            self.cursor.close()
        # 没有不同
        elif self.Tos == 1:
            sql = "INSERT INTO work (company,time,local,experience,Education,position,salary,Lure,key,workUrl,description,vk) " \
                  "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d')"
            sqlData = (self.company,self.releaseTime,self.local,self.experience,self.Education,self.position,self.salary
                       ,self.Lure,self.key,self.workUrl,self.description,1)
            self.cursor.execute(sql%sqlData)
            self.connect.commit()
            self.cursor.close()
    def inspectData(self):
        sql = 'select * from work where company = '+ self.company + 'and position ='+ self.position + '' \
                    'and salary = ' + self.salary
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        lens = len(data)

        if lens == 1:
            if data[0][2] == self.releaseTime:
                self.Tos = 3
            else:
                self.Tos = 2
                self.id = data[0][0]
        else:
            self.Tos = 1



