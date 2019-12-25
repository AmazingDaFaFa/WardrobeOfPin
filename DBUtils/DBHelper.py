from operator import index

import pymysql
import re
import dictionary
from django import db

from test1 import cur


class DBHelper:

    def __init__(self, host="localhost", username="root", password="?!ntqoKYQ0iL", port=3306, database="yigui"):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.con = None
        self.cur = None
        try:
            self.con = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=self.port,
                                   db=self.database)
            # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
            self.cur = self.con.cursor()
        except:
            raise Exception("DataBase connect error,please check the db config.")

    def get_index_dict(cur):
        index_dict = dict()
        index = 0
        for desc in cur.description:
            index_dict[desc[0]] = index
            index = index + 1
        return index_dict
    def close(self):
        #关闭连接

        if not  self.con:
            self.con.close()
        else:
            raise Exception("DataBase doesn't connect,close connectiong error;please check the db config.")

    def commit(self):
        self.conn.commit()

    def get_dict_data_sql(cursor, sql):
        """
        运行sql语句，获取结果，并根据表中字段名，转化成dict格式（默认是tuple格式）
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        index_dict = cursor.get_index_dict(cursor)
        res = []
        for datai in data:
            resi = dict()
            for indexi in index_dict:
                resi[indexi] = datai[index_dict[indexi]]
            res.append(resi)
        return res

    def login(username,password):

        try:
            cur.execute("select*  from User where UserName='%s' "%username)
            user = cur.fetchone()
            password1 = password
            password2=  user[3]
            if user is None:
                return -1
                print("用户不存在")
            if password1!=password2:
                return 0
                print("ERROR PASSWORD")

        except:
            raise Exception('MySQL execute failed! ERROR ')
    def register(username, password, sex, height, weight):
        cur.execute("select*  from User where UserName='%s' " % username)

        sql ="insert into User values(%s,%s,%s,%s,%s)"
        try:

            cur.execute(sql,username,password,sex,height,weight)
            db.commit()
            cur.execute()

        except:

    def add_clothes_data(image_data, color, category):
        sql = "insert into clothes values(%s,%s,%s,%s)"
        try:
            cur.execute(sql,(image_data,color,category))

            return
        except:
            raise Exception('add clothes error')



    def delete_clothes_data(clothes_id):
        sql = "delete from clothes where ClotheId=%s"
        try:
            cur.execute(sql,clothes_id)
            result=

    def get_clothes_data(category):


    def update_clothes_data(clothes_id, image_data, color, category):
        sql = "update clothes " \
              "set Image_Data='%s',Color='%s',Category='%s'" \
              "where ClotheId='%s'"
        try:
            cur.execute(sql,(image_data,color,category,clothes_id))
            db.commit()
            results = cur.fetchone(clothes_id)
            cur.close()
        except:
          raise Exception('update_clothes_ failed! ERROR ')



    def get_user_data(user_id):
        try:
            sql = "select* from user where UserId='%s'"
            cur.execute(sql,(user_id))
            user_data=cur.fetchone()
            return user_data
        except:
            raise Exception('get user data failed!')
    def update_user_data(user_id, user_nickname, user_portraits, user_sex, user_age, user_height, user_weight):
        sql = "update user" \
              "set UserId='%s',UserNickname='%s,UserPortraits='%s',UserSex='%s',UserAge='%s',UseHeight='%s',UserWeight='%s'" \
              "where UserId='%s'"
        try:
            cur.execute(sql.(user_id,user_nickname,user_portraits,user_sex,user_age,user_height,user_weight,user_id))
            if
            return
        except:
            raise Exception('update user data failed!')

    def get_user_collection(user_id, count):
        try:
            cur.execute("select* from collection where UserId='%s'"%user_id)#通过用户ID寻找收藏
            collection_data=cur.fetchone()
            cur.execute("select ClothesId from outfitclothes where OutfitId='%s'"%collection_data[2])#通过收藏ID寻找服装
            clothes_data = cur.fetchall()

            index_dict = collection_data.get_index_dict(cur)
            cur.close()
            res = []
            for datai in clothes_data:
                resi = dict()
                for indexi in index_dict:
                    resi[indexi] = datai[index_dict[indexi]]
                res.append(resi)

        except:
            raise Exception('update user collection failed!')


    def get_outfit_data(user_id, outfit_id):
        try:
            cur.execute("select* from outfit left out join outfitclothes where OutfitId='%s'" % outfit_id)
            outfit_data=cur.fetchone()
            return outfit_data
        except:
            raise Exception('get_outfit_ failed! ERROR ')


    def set_outfit_favour(user_id, outfit_id):
        sql = ""

    def get_history_data_by_count(user_id, count):