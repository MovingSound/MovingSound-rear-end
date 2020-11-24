import pymysql


def scan(telephone, passwd):
    con = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456',
                          db='DongSheng', charset='utf8')
    cursor = con.cursor(pymysql.cursors.DictCursor)
    try:
        sql = 'select passwd from user where username='+telephone
        cursor.execute(sql)
        result = cursor.fetchall()
        right_passwd = result[0]['passwd']
        if right_passwd == passwd:
            print('***即将进入动声音乐***')
        else:
            print('用户名或者密码错误')
    except Exception:
        print("用户名不存在")
    con.commit()
    con.close()


telephone = input("输入你的账号：")
passwd = input("输入你的密码：")
scan(telephone, passwd)