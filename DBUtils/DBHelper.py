import pymysql
import cv2
import time
import os


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

    def login(self, username, password):
        try:
            self.cur.execute("SELECT * FROM User WHERE UserName='%s' " % username)
            user = self.cur.fetchone()
            if user is None:
                return -1
                print("用户不存在")
            if password != user[3]:
                return 0
                print("ERROR PASSWORD")
            return user[0]
        except:
            raise Exception('MySQL execute failed! ERROR ')

    def register(self, username, password, sex, height, weight):
        self.cur.execute("SELECT * FROM User WHERE UserName='%s' " % username)
        user = self.cur.fetchall()
        if user is None:
            return -1

        sql = "INSERT INTO User(UserName, Password, Sex, Height, Weight) VALUES (%s,%s,%s,%s,%s)"
        try:
            self.cur.execute(sql, (username, password, sex, height, weight))
            self.db.commit()
            self.cur.execute()
            return self.cur.fetchone()[0]
        except:
            pass

    def add_clothes_data(self, image_data, color, category):
        sql = "INSERT INTO clothes(ImageUrl,Color,Category) VALUES (%s,%s,%s)"

        date = time.time()[:8]
        image_url = './root/clothes/' + date + '.png'
        cv2.imwrite(image_url, image_data)  # 后端执行此段代码，路径入库，图片存到对应路径

        try:
            self.cur.execute(sql, (image_url, color, category))
            return True
        except:
            raise Exception('add clothes error')
            return False

    def delete_clothes_data(self, clothes_id):
        sql_select = "SELECT * FROM clothes WHERE ClothesId=%s"
        sql_delete = 'DELETE FROM clothes WHERE ClothesId=%s'
        try:
            self.cur.execute(sql_select, clothes_id)
            clothes_image = self.cur.fetchone()

            dirPath = './root/clothes/' + clothes_image[1] + '.png'
            # 判断文件是否存在
            if os.path.exists(dirPath):
                os.remove(dirPath)
            else:
                print("要删除的文件不存在！")

            self.cur.execute(sql_delete, clothes_id)
            return True
        except:
            return False

    def get_clothes_data(self, category):
        sql = "SELECT * FROM clothes WHERE Category = '%s'"
        result = []
        try:
            self.cur.execute(sql, category)
            clothes_list = self.cur.fetchall()

            for clothes in clothes_list:
                clothes_dict = {'clothes_id': clothes[0], 'clothes_image': clothes[1], 'clothes_color': clothes[2],
                                'clothes_category': clothes[3]}
                result.append(clothes_dict)
            return result
        except:
            print('获取数据失败')

    def update_clothes_data(self, clothes_id, image_data, color, category):
        sql_update = "UPDATE clothes SET Image_Data='%s',Color='%s',Category='%s' WHERE ClotheId='%s'"
        sql_select = "SELECT * FROM clothes WHERE ClothesId = '%s'"

        date = time.time()[:8]
        image_url = './root/clothes/' + date + '.png'
        cv2.imwrite(image_url, image_data)  # 后端执行此段代码，路径入库，图片存到对应路径

        try:
            self.cur.execute(sql_select, clothes_id)
            clothes_image = self.cur.fetchone()

            dirPath = './root/clothes/' + clothes_image[1] + '.png'
            # 判断文件是否存在
            if os.path.exists(dirPath):
                os.remove(dirPath)
            else:
                print("要删除的文件不存在！")

            self.cur.execute(sql_update, (image_data, color, category, clothes_id))
            self.db.commit()
            results = self.cur.fetchone()[0]

            return results
        except:
            raise Exception('update_clothes_ failed! ERROR ')

    def get_user_data(self, user_id):
        try:
            sql = "SELECT * FROM user WHERE UserId='%s'"
            self.cur.execute(sql, user_id)
            user = self.cur.fetchone()
            user_data = {'user_id': user[0], 'user_name': user[1], 'user_nickname': user[3], 'user_portraits': user[4],
                         'user_sex': user[5], 'user_age': user[6], 'user_height': user[7], 'user_weight': user[8]}

            return user_data
        except:
            raise Exception('get user data failed!')

    def update_user_data(self, user_id, user_nickname, user_portraits, user_sex, user_age, user_height, user_weight):
        sql_update = "UPDATE user SET UserId='%s',UserNickname='%s',UserPortraits='%s',UserSex='%s',UserAge='%s',UseHeight='%s',UserWeight='%s' WHERE UserId='%s'"
        sql_select = "SELECT * FROM user WHERE UserId='s'"
        try:

            # 存储新头像
            date = time.time()[:8]
            image_url = './root/user/' + date + '.png'
            cv2.imwrite(image_url, user_portraits)  # 后端执行此段代码，路径入库，图片存到对应路径

            # 查找旧头像文件，删除旧文件
            self.cur.execute(sql_select, user_id)
            user = self.cur.fetchone()

            dirPath = './root/user/' + user[4] + '.png'
            # 判断文件是否存在
            if os.path.exists(dirPath):
                os.remove(dirPath)
            else:
                print("要删除的文件不存在！")

            # 更新数据库信息
            self.cur.execute(sql_update,
                             (user_id, user_nickname, user_portraits, user_sex, user_age, user_height, user_weight))
            self.db.commit()

        except:
            raise Exception('update user data failed!')

    def get_user_collection(self, user_id, count):
        try:
            self.cur.execute("SELECT * FROM collection WHERE UserId='%s'" % user_id)  # 通过用户ID寻找收藏
            collections = self.cur.fetchall()

            result = []

            for collection in collections:
                self.cur.execute("SELECT * FROM outfit WHERE OutfitId='%s'" % collection[2])
                outfits = self.cur.fetchall()
                outfit_list = []
                for outfit in outfits:
                    self.cur.execute("SELECT * FROM outfitclothes WHERE OutfitId='%s'" % outfit[2])
                    clothes_outfit = self.cur.fetchall()
                    clothes_list = []
                    for clothes in clothes_outfit:
                        self.cur.execute("SELECT * FROM clothes WHERE ClothesId='%s'" % clothes[1])
                        clothes_item = self.cur.fetchall()
                        clothes_list.append({'clothes_id': clothes_item[0], 'clothes_image': clothes_item[1],
                                             'clothes_color': clothes_item[2], 'clothes_category': clothes_item[3]})
                    outfit_list.append({
                        'outfit_id': outfit[2],
                        'clothes': clothes_list,
                        'outfit_date': outfit[0],
                        'outfit_trip': outfit[3]
                    })
                result = outfit_list

            return result
        except:
            raise Exception('update user collection failed!')

    def set_outfit_favour(self, user_id, outfit_id):
        sql_add_favour = "INSERT INTO collection(UserId, OutfitId, Date) VALUES (%s, %s, %s)"

        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.cur.execute(sql_add_favour, (user_id, outfit_id, date))

        return True

    def get_history_data_by_count(self, user_id, count):
        self.cur.execute("SELECT * FROM outfit WHERE UserId='%s'" % user_id)
        outfits = self.cur.fetchall()
        outfit_list = []
        for outfit in outfits:
            self.cur.execute("SELECT * FROM outfitclothes WHERE OutfitId='%s'" % outfit[2])
            clothes_outfit = self.cur.fetchall()
            clothes_list = []
            for clothes in clothes_outfit:
                self.cur.execute("SELECT * FROM clothes WHERE ClothesId='%s'" % clothes[1])
                clothes_item = self.cur.fetchall()
                clothes_list.append({'clothes_id': clothes_item[0], 'clothes_image': clothes_item[1],
                                     'clothes_color': clothes_item[2], 'clothes_category': clothes_item[3]})
            outfit_list.append({
                'outfit_id': outfit[2],
                'clothes': clothes_list,
                'outfit_date': outfit[0],
                'outfit_trip': outfit[3]
            })
        result = outfit_list

        return result
