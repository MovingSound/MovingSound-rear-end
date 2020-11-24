import pymysql


def register(DSid, telephone, passwd):
    cursor.execute("insert into user (DSid,username,passwd) values( %s, % s, % s)", (DSid, telephone, passwd))


def userID():
    # 查询user表格
    sql = 'select max(DSid) from user'
    cursor.execute(sql)
    result = cursor.fetchall()
    # DSid为最后一个id
    DSid = result[0]['max(DSid)']
    count = DSid + 1
    print("注册成功！")
    print("用户id为" + str(count))
    con.commit()
    con.close()
    return count


def examine(tel):
    # 查询user表格
    sql = 'select username from user'
    cursor.execute(sql)
    result = cursor.fetchall()
    for li in result:
        if li['username'] == str(tel):
            print("用户名重复")
            exit()


con = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456',
                          db='DongSheng', charset='utf8')
cursor = con.cursor(pymysql.cursors.DictCursor)

telephone = eval(input("输入你的账号："))
examine(telephone)
passwd = input("输入你的密码：")
DSid = userID()
register(DSid, telephone, passwd)

con.commit()
con.close()