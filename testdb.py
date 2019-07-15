import pymysql

class MySQLCommand(object):
    # 类的初始化
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306  # 端口号
        self.user = 'root'  # 用户名
        self.password = "979818137zzn"  # 密码
        self.db = "gkdb"  # 库
        self.table = "gkprdata"  # 表

    # 链接数据库
    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()
            print('数据库这里连接成功了')
        except:
            print('connect mysql error.')

    def insertData(self, my_dict):
        # table = "gkprdata"  # 要操作的表格
        # 注意，这里查询的sql语句url=' %s '中%s的前后要有空格

        sqlExit = "SELECT profession_name,school_name,years  FROM " + self.table + " WHERE profession_name= '" + \
                  my_dict['profession_name'] + "'""and school_name='" + my_dict['school_name'] + "'""and years='" + my_dict[
                      'years'] + "'"

        res = self.cursor.execute(sqlExit)
        print(sqlExit)
        self.conn.commit()
        print(res)
        if res:  # res为查询到的数据条数如果大于0就代表数据已经存在
             print("数据已存在", res)
             return 0
        # 数据不存在才执行下面的插入操作
        try:
            cols = ', '.join(my_dict.keys())  # 用，分割
            values = '","'.join(my_dict.values())
            sql = "INSERT INTO " + self.table + " (%s) VALUES (%s)" % (cols, '"' + values + '"')
            print(sql)
        #     # 拼装后的sql如下
        #     # INSERT INTO gkprdata (profession_name, school_name, average_score, hightest_score, student_area, subject, years, batch) VALUES ("专业测试"," 校名测试"," 0"," 750"," 考生地区测试","
            # 科目测试"," 2019"," 第一批")
            try:
                 result = self.cursor.execute(sql)
                 insert_id = self.conn.insert_id()  # 插入成功后返回的id
                 self.conn.commit()
                 # 判断是否执行成功
                 if result:
                     print("插入成功", insert_id)
                     return insert_id + 1
            except pymysql.Error as e:
                 # 发生错误时回滚
                 self.conn.rollback()
                 # 主键唯一，无法插入
                 if "key 'PRIMARY'" in e.args[1]:
                     print("数据已存在，未插入数据")
                 else:
                     print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
             print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    def getLastId(self):
        sql = "SELECT max(id) FROM " + self.table
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()  # 获取查询到的第一条数据
            if row[0]:
                return row[0]  # 返回最后一条数据的id
            else:
                return 0  # 如果表格为空就返回0
        except:
            print(sql + ' execute failed.')

    def closeMysql(self):
        self.cursor.close()
        self.conn.close()  # 创建数据库操作类的实例

