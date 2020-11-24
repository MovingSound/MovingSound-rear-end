import pymysql

class create():
    def create_database(self):
        try:
            self.cursor.execute("drop database if exists MovingSound;")
            self.cursor.execute("create database MovingSound;")
            self.cursor.execute("use MovingSound;")
        except Exception as err:
            print(err)

    def create_msg(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS msg;")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS msg(mid varchar(32) PRIMARY KEY,"   # 歌曲号
                            "mname varchar(20) NOT NULL,"                                       # 歌曲名
                            "mfeature varchar(20) NOT NULL,"                                    # 歌曲特征向量
                            "mtype varchar(20) NOT NULL,"                                       # 歌曲风格标签
                            "mpath varchar(100) NOT NULL,"                                      # 存储路径
                            "mlanguage varchar(20),"                                            # 语种
                            "mtime varchar(20) NOT NULL,"                                       # 歌曲时间
                            "mpicture longblob,"                                                # 歌曲封面
                            "mdate varchar(20) NOT NULL);")                                       # 歌曲发行日期
        except Exception as err:
            print(err)

    def create_feedback(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS feedback;")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS feedback(uid varchar(32) PRIMARY KEY);")    # 用户号
            # 后续获取用户对某首歌的反馈就增加一列，值为1为喜欢，值为0则为不喜欢
        except Exception as err:
            print(err)

    def insert_feedback_like(self,uid,song_name):
        try:
            self.cursor.execute("alter table feedback add column" + song_name + " varchar(2) not null")
            sql = "insert into feedback (uid,column"+song_name+") value ("+str(uid)+","+str(1)+")"
            self.cursor.execute(sql)
        except Exception as err:
            print(err)

    def insert_feedback_dislike(self,uid,song_name):
        try:
            self.cursor.execute("alter table feedback add column" + song_name + " varchar(2) not null")
            sql = "insert into feedback (uid,column"+song_name+") value ("+str(uid)+","+str(0)+")"
            self.cursor.execute(sql)
        except Exception as err:
            print(err)

    def insert_msg(self,mid,mname,mfeature,mtype,mpath,mlanguage,mtime,mpicture,mdate):
        try:
            self.cursor.execute(
                "insert into mooc(mid,mname,mfeature,mtype,mpath,mlanguage,mtime,mpicture,mdate) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (mid,mname,mfeature,mtype,mpath,mlanguage,mtime,mpicture,mdate))
        except Exception as err:
            print(err)

    def test(self):
        self.con = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="mydb",
                                   charset="utf8")
        self.cursor = self.con.cursor(pymysql.cursors.DictCursor)
        #self.create_database()
        #self.create_msg()
        #self.create_feedback()
        #self.insert_feedback_like(123,name)
        #self.con.commit()
        #self.insert_msg
        print("complete")

name = "123"
create().test()


