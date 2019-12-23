import requests
import json
import base64
import numpy as np
import cv2

#将图片数据转成base64格式

# with open('/root', 'rb') as f:
#     img = base64.b64encode(f.read()).decode()
# image = []
# image.append(img)
# res = {"image": image}

j_data = {"username": "abc", "password": "123"}

# headers = {'Content-Type': 'application/x-www-form-urlencoded'}
# headers = {'Content-Type': 'multipart/form-data'}
headers = {'Content-Type': 'application/json'}

image = open('../static/IMG.jpg', 'rb')


files = {
    'image': base64.b64encode(image.read()).decode('ascii')
}

j_data.update(files)

# 访问服务
r = requests.post(url='http://127.0.0.1:8080/update_user_info', headers=headers, data=json.dumps(j_data))

# image.close()
data = json.loads(r.text)
print(data)
