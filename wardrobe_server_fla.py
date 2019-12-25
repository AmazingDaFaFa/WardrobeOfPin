from flask import Flask, request, jsonify
import json
import base64
import cv2
import numpy as np
from crawler import crawler_weather
# from DBUtils import DBHelper


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def test():
    return json.dumps({'result': '服务器正常运行'}, ensure_ascii=False)


@app.route('/user_login', methods=['POST', 'GET'])
def user_login():
    data_input_json = json.loads(request.get_data())

    user_id = 1

    # TODO 调用数据库登录接口----login(username, password) 返回值 user_id，若为0则表示密码不正确，若为-1则表示用户不存在
    # user_id = DBHelper.DBHelper.login(data_input_json['username'], data_input_json['password'])

    data_output_json = {'user_id': user_id}

    return jsonify(data_output_json)


@app.route('/user_register', methods=['POST', 'GET'])
def user_register():
    data = request.get_data()
    data_input_json = json.loads(data)

    # TODO 调用数据库注册函数----register(username, password, sex, height, weight) 返回值user_id
    user_id = 1

    # user_id = DBHelper.DBHelperregister(data_input_json['username'], data_input_json['password'], data_input_json['sex']
    #                                     , data_input_json['height'], data_input_json['weight'])

    data_output_json = {'user_id': user_id}

    return json.dumps(data_output_json, ensure_ascii=False)


@app.route('/add_clothes', methods=['POST', 'GET'])
def add_clothes():
    data = request.get_data()
    data_input_json = json.loads(data)

    # 解析图片数据
    img = data_input_json['image']
    img_decode_ = img.encode('ascii')  # ascii编码
    img_decode = base64.b64decode(img_decode_)  # base64解码
    img_np = np.frombuffer(img_decode, np.uint8)  # 从byte数据读取为np.array形式
    image_data = cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)  # 转为OpenCV形式


    # cv2.imwrite('/root/01.png', image_data) # 后端执行此段代码，路径入库，图片存到对应路径
    # TODO 调用数据库添加服装函数----add_clothes_data(image_data, color, category) 返回值true|false

    data_output_json = {'add_clothes': 'succeed'}

    # data_output_json.update({'result': add_clothes_data(image_data, data_input_json['color'], data_input_json['category'])})

    return json.dumps(data_output_json, ensure_ascii=False)


@app.route('/get_clothes', methods=['POST', 'GET'])
def get_clothes():
    data_input_json = json.loads(request.get_data())
    data_output_json = {}

    # TODO 调用数据库获取服装函数----get_clothes_data(category)
    # 返回值[{'clothes_id':, 'clothes_image':, 'clothes_color':, 'clothes_category':}, {}, ]

    # data_output_json = {'clothes_list': get_clothes_data(data_input_json['category']}

    return json.dumps(data_output_json, ensure_ascii=False)


@app.route('/delete_clothes', methods=['POST', 'GET'])
def delete_clothes():
    data_input_json = json.loads(request.get_data())
    data_output_json = {}

    # TODO 调用数据库删除服装函数----delete_clothes_data(clothes_id) 返回值true|false

    # data_output_json = {'result': delete_clothes_data(data_input_json['clothes_id'])}

    return json.dumps(data_output_json, ensure_ascii=False)


@app.route('/update_clothes', methods=['POST', 'GET'])
def update_clothes():
    data_input_json = json.loads(request.get_data())
    data_output_json = {}

    # 解析图片数据
    img = data_input_json['image']
    img_decode_ = img.encode('ascii')  # ascii编码
    img_decode = base64.b64decode(img_decode_)  # base64解码
    img_np = np.frombuffer(img_decode, np.uint8)  # 从byte数据读取为np.array形式
    image_data = cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)  # 转为OpenCV形式

    # TODO 调用数据库更新服装函数----update_clothes_data(clothes_id, image_data, color, category) 返回值clothes_id

    # data_output_json.update({'clothes_id': update_clothes_data(data_input_json['clothes_id'], image_data, data_input_json['color'], data_input_json['category'])})

    return json.dumps(data_output_json, ensure_ascii=False)


@app.route('/get_user', methods=['POST', 'GET'])
def get_user():
    data_input_json = json.loads(request.get_data())
    data_output_json = {}

    # TODO 调用数据库获取用户函数----get_user_data(user_id)
    # 返回值{'user_id':, 'user_name':, 'user_nickname':, 'user_portraits':, 'user_sex':, 'user_age':, 'user_height':, 'user_weight':}

    # data_output_json.update(get_user_data(data_input_json['user_id'])

    return json.dumps(data_output_json, ensure_ascii=False)


@app.route('/update_user_info', methods=['POST', 'GET'])
def update_user_info():
    data_input_json = json.loads(request.get_data())
    data_output_json = {}

    # 解析图片数据
    image_data = convert_image_encode(data_input_json['image'])

    # TODO 调用数据库更新用户信息函数----update_user_data(user_id, user_nickname, user_portraits, user_sex, user_age, user_height, user_weight) 返回值true|false

    # data_output_json.update({'result': update_user_data(data_input_json['user_id'], data_input_json['user_nickname'],
    #                                                     image_data, data_input_json['user_sex'],
    #                                                     data_input_json['user_age'], data_input_json['user_height'],
    #                                                     data_input_json['user_weight'])})

    return json.dumps(data_output_json, ensure_ascii=False)


@app.route('/get_collection', methods=['POST', 'GET'])
def get_collection():
    data_input_json = json.loads(request.get_data())
    data_output_json = {}

    # TODO 调用数据库获取收藏函数----get_user_collection(uid, count) [数据库根据count返回id > count的内容]
    # 返回值[{'outfit_id':, 'clothes':[<clothes0>, <clothes1>, ], 'outfit_date':, 'outfit_trip':}, {}, ]

    # data_output_json.update({'outfits': get_user_collection(data_input_json['user_id'], data_input_json['count'])})

    return json.dumps(data_output_json, ensure_ascii=False)


@app.route('/get_outfit', methods=['POST', 'GET'])
def get_outfit():
    data_input_json = json.loads(request.get_data())
    data_output_json = {}

    # TODO 调用数据库获取穿搭函数----get_outfit_data(uid, oid) 返回值{'outfit_id':, 'clothes':[<clothes0>, <clothes1>, ], 'outfit_date':, 'outfit_trip':}
    # data_output_json.update(get_outfit_data(data_input_json['user_id'], data_input_json['outfit_id']))

    return json.dumps(data_output_json, ensure_ascii=False)


@app.route('/create_new_outfit', methods=['POST', 'GET'])
def create_new_outfit():
    data_input_json = json.loads(request.get_data())
    data_output_json = {}

    # # 读入json数据 uid、city、trip、mood
    # data_input_json.update({'uid', request.form['uid']})
    # data_input_json.update({'city', request.form['city']})
    # data_input_json.update({'trip', request.form['trip']})
    # data_input_json.update({'mood', request.form['mood']})

    # 爬取天气信息，得到天气字典weather_data = {'city':, 'weather':, 'max_temp':, 'min_temp':}
    spider = crawler_weather.WeatherCrawler()
    weather_data = spider.getTemp_city(data_input_json['city'])

    data_input_json.update(weather_data)

    # TODO 调用数据库方法----checkWeather(weather, max_temp, min_temp) 返回值 categorys = [category1, category2, ...]
    # TODO 调用数据库方法----checkMood(mood) 返回值 colors = [color1, color2, ...]
    # TODO 调用数据库方法----get_popular_color() 返回值 color_p = [color1, color2, ...]

    # colors.append(color_p)

    # TODO get_clothes_category_color(categorys = [], colors = [], uid) 返回值[cid1, cid2, ...]
    # category_s = '('
    # for category in categorys:
    #   category_s += 'CLOTHES.category = ' + category + 'or '
    # else
    #   category_s += ')'
    # color同上
    # 'SELECT CID FROM CLOTHES WHERE uid = uid and ? and ? ', values(%s, %s), category_s, color_s



    # TODO 调用数据库对应方法 create_outfit(data_input_json)

    return json.dumps(data_output_json, ensure_ascii=False)


@app.route('/add_to_favour', methods=['POST', 'GET'])
def add_to_favour():
    data_input_json = json.loads(request.get_data())
    data_output_json = {}

    # TODO 调用数据库方法----set_outfit_favour(uid, outfit_id) 返回值true|false

    # data_output_json.update({'result': set_outfit_favour(data_input_json['user_id'], data_input_json['outfit_id'])})

    return json.dumps(data_output_json, ensure_ascii=False)


@app.route('/get_history', methods=['POST', 'GET'])
def get_history():
    data_input_json = json.loads(request.get_data())
    data_output_json = {}

    # TODO 调用数据库获取历史记录方法----get_history_data_by_count(user_id, count) [数据库根据count返回id > count的内容]
    # 返回值[{'outfit_id':, 'clothes':[<clothes0>, <clothes1>, ], 'outfit_date':, 'outfit_trip':}, {}, ]

    # data_output_json.update({'history_outfits': get_history_data_by_count(data_input_json['user_id'], data_input_json['count'])})

    return json.dumps(data_output_json, ensure_ascii=False)


def convert_image_encode(image_str):
    img = image_str
    img_decode_ = img.encode('ascii')  # ascii编码
    img_decode = base64.b64decode(img_decode_)  # base64解码
    img_np = np.frombuffer(img_decode, np.uint8)  # 从byte数据读取为np.array形式
    return cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)  # 转为OpenCV形式


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
