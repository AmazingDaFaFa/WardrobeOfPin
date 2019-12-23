from bs4 import BeautifulSoup
import requests
import random
import time
import socket
import http.client


class WeatherCrawler:
    def __init__(self):
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, sdch',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        'Connection': 'keep-alive',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/43.0.235'}  # 设置头文件信息
        self.urls = ['http://www.weather.com.cn/textFC/hb.shtml',
                     'http://www.weather.com.cn/textFC/db.shtml',
                     'http://www.weather.com.cn/textFC/hd.shtml',
                     'http://www.weather.com.cn/textFC/hz.shtml',
                     'http://www.weather.com.cn/textFC/hn.shtml',
                     'http://www.weather.com.cn/textFC/xb.shtml',
                     'http://www.weather.com.cn/textFC/xn.shtml']

    # 启动函数，开始爬取所有城市今天的天气
    def getTemp_Nation(self):
        for url in self.urls:
            self.get_temperature(url)
        print('<-----------爬取今日天气成功！----------->')

    # 启动函数，开始爬取指定城市今天的天气
    def getTemp_city(self, city_name):
        url = self.get_url(city_name)
        html = self.get_content(url)
        return self.get_data_future(html, city_name)

    # 启动函数，开始爬取制定城市未来七点的天气情况
    def getTemp_Future(self, city_name):
        url = self.get_url(city_name)
        html = self.get_content(url)
        self.get_data_future(html, city_name)
        print('<-----------爬取未来7天天气信息成功！------------>')
        # db.close()

    # 启动函数，开始爬取指定城市的生活信息
    def getGuide(self, city_name):
        # self.cursor.execute('DELETE FROM LifeGuide')
        url = self.get_url_1d(city_name)  # 获取城市天气的url
        html = self.get_content(url)  # 获取网页html
        self.get_data_guide(html, city_name)  # 爬取城市的信息
        print('<--------------------爬取生活指南成功！--------------------->')

    # 爬取天气信息（气象，温度，风向） # 入库
    def get_temperature(self, url):
        response = requests.get(url, headers=self.headers).content  # 提交requests get 请求
        soup = BeautifulSoup(response, "lxml")  # 用Beautifulsoup 进行解析
        conmid = soup.find('div', class_='conMidtab')
        conmid2 = conmid.findAll('div', class_='conMidtab2')
        for info in conmid2:
            tr_list = info.find_all('tr')[2:]  # 使用切片取到第三个tr标签
            for index, tr in enumerate(tr_list):  # enumerate可以返回元素的位置及内容
                td_list = tr.find_all('td')
                if index == 0:
                    province_name = td_list[0].text.replace('\n', '')  # 取每个标签的text信息，并使用replace()函数将换行符删除
                    city_name = td_list[1].text.replace('\n', '')
                    weather = td_list[5].text.replace('\n', '')
                    wind = td_list[6].text.replace('\n', '')
                    max = td_list[4].text.replace('\n', '')
                    min = td_list[7].text.replace('\n', '')
                    # print(province_name)
                else:
                    city_name = td_list[0].text.replace('\n', '')
                    weather = td_list[4].text.replace('\n', '')
                    wind = td_list[5].text.replace('\n', '')
                    max = td_list[3].text.replace('\n', '')
                    min = td_list[6].text.replace('\n', '')

                print(city_name, weather, wind, max, min)

                # TODO 暂存数据到服务器即可

                return city_name, weather, wind, max, min

                # self.cursor.execute('INSERT INTO NowadaysWeather_Nation(cityName,weather,wind,maxTemp,minTemp) '
                #                'VALUES(%s,%s,%s,%s,%s)', (city_name, weather, wind, max, min))

    # 获取每个城市对应天气的url（对应主页网址）
    def get_url(self, city_name):
        url = 'http://www.weather.com.cn/weather/'
        with open('./crawler/city.txt', 'r', encoding='gb2312') as fs:
            # utf-8不行，改用gb2312国际码编码。city.txt下保存每个城市
            lines = fs.readlines()
            # readlines() 方法用于读取所有行(直到结束符 EOF)并返回列表
            for line in lines:
                if (city_name in line):
                    code = line.split('=')[0].strip()
                    # 以等号为分隔符,将字符串分割，如101010100=北京 被分割为｛101010100，北京｝，而[0]指取第一个数字，保存在code里
                    return url + code + '.shtml'
                line.split()
        raise ValueError('invalid city name')  ##非法的城市名

    # 获取每个城市对应天气的url（对应城市1day页面）
    def get_url_1d(self, city_name):
        url = 'http://www.weather.com.cn/weather1d/'
        with open('./city.txt', 'r', encoding='gb2312') as fs:
            # utf-8不行，改用gb2312国际码编码。city.txt下保存每个城市
            lines = fs.readlines()
            # readlines() 方法用于读取所有行(直到结束符 EOF)并返回列表
            for line in lines:
                if (city_name in line):
                    code = line.split('=')[0].strip()
                    # 以等号为分隔符,将字符串分割，如101010100=北京 被分割为｛101010100，北京｝，而[0]指取第一个数字，保存在code里
                    return url + code + '.shtml'
                line.split()
        raise ValueError('invalid city name')  ##非法的城市名

    # 对网页获取get请求，得到的是response对象
    def get_content(self, url, data=None):
        #  模拟浏览器访问
        #  超时，取随机数是因为防止被网站认定为网络爬虫
        timeout = random.choice(range(80, 180))
        while True:
            try:
                #  获取请求数据
                rep = requests.get(url, headers=self.headers, timeout=timeout)
                rep.encoding = 'utf-8'
                break
            except socket.timeout as e:
                print('3:', e)
                time.sleep(random.choice(range(8, 15)))
            except socket.error as e:
                print('4:', e)
                time.sleep(random.choice(range(20, 60)))
            except http.client.BadStatusLine as e:
                print('5:', e)
                time.sleep(random.choice(range(30, 80)))
            except http.client.BadStatusLine as e:
                print('6:', e)
                time.sleep(random.choice(range(5, 15)))

        return rep.text

    # 获取html中我们所需要的字段：
    def get_data_future(self, html_text, city_name):

        bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象，解析器为：html.parser
        body1 = bs.body  # 获取body部分

        #  print(body1)
        data = body1.find('div', {'id': '7d'})  # 找到id为7d的div
        ul = data.find('ul')  # 获取ul部分
        li = ul.find_all('li')  # 获取所有的li

        # identi = 1

        for day in li[:1]:  # 对每个li标签中的内容进行遍历
            #  添加日期
            data = day.find('h1').string  # 找到日期
            Date = data.split('（')[0]

            inf = day.find_all('p')  # 找到li中的所有p标签

            #  添加天气状况
            weather = inf[0].string

            #  添加最高气温
            if inf[1].find('span') is None:
                temperature_highest = None  # 天气当中可能没有最高气温（傍晚）
                maxTemp = ''
            else:
                temperature_highest = inf[1].find('span').string  # 找到最高气温
                temperature_highest = temperature_highest.replace('℃', '')
                maxTemp = temperature_highest
                # 最高气温其实没有这个温度符号，有没有这个替换都没事

            # 添加最低气温
            temperature_lowest = inf[1].find('i').string  # 找到最低温
            temperature_lowest = temperature_lowest.replace('℃', '')  # 最低温度后面有个℃，去掉这个符号

            minTemp = temperature_lowest

            # self.cursor.execute('INSERT INTO FutureWeather_City(cityName, date, weather, maxTemp, minTemp) '
            #                'VALUES (%s,%s,%s,%s,%s)', (city_name, Date, weather, maxTemp, minTemp))
            # self.db.commit()
            # ++identi
            print(city_name, Date, weather, maxTemp, minTemp)
            temp_info = {'city': city_name, 'weather': weather, 'max_temp': maxTemp, 'min_temp': minTemp}
        return temp_info

    # 爬取网页上的城市生活信息  # 入库
    def get_data_guide(self, html_text, city_name):
        #  final元组存放一天的数据
        t = []
        t.append(city_name)
        bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象，解析器为：html.parser
        body = bs.body  # 获取body部分

        #  print(body1)
        data = body.find('div', {'class': 'livezs'})  # 找到class为livezs的div
        ul = data.find('ul')  # 获取ul部分
        li = ul.find_all('li')  # 获取所有的li

        for day in li:  # 对每个li标签中的内容进行遍历
            inf = day.find_all('p')  # 找到li中的所有p标签

            temp = inf[0].string
            # self.cursor.execute('INSERT INTO LifeGuide(City, Suggestion) VALUES (%s, %s)', (city_name, temp))
            # self.db.commit()


if __name__ == '__main__':
    weatherCralwer = WeatherCrawler()
    weatherCralwer.getTemp_city('汉中')


# main()
