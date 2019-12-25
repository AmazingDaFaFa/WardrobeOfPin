import pymysql
conn=pymysql.connect('localhost','root','123456')
conn.select_db('yigui')
#获取游标
cur=conn.cursor()
update=cur.execute("update user set UserId=1 where UserName='牛蛙克克'")
print ('修改后受影响的行数为：',update)
cur.close()
conn.commit()
conn.close()