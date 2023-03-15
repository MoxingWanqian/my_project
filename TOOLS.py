# 导入库
from time import sleep
from requests import get
from random import choice
from bs4 import BeautifulSoup
from selenium import webdriver
from time import localtime as tm

# 随机请求头函数
def headers_random():
    header_list = [
        # pc端的user-agent
        # 谷歌
        'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.html.2171.71 '
        'Safari/537.36',
        'Mozilla/5.0.html (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.html.1271.64 '
        'Safari/537.11',
        'Mozilla/5.0.html (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) '
        'Chrome/10.0.html.648.133 Safari/534.16',
        # 火狐
        'Mozilla/5.0.html (Windows NT 6.1; WOW64; rv:34.0.html) Gecko/20100101 Firefox/34.0.html',
        'Mozilla/5.0.html (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) '
        'Firefox/3.6.10',
        # opera
        'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.html.2171.95 '
        'Safari/537.36 OPR/26.0.html.1656.60',
        # qq浏览器
        'Mozilla/5.0.html (compatible; MSIE 9.0.html; Windows NT 6.1; WOW64; Trident/5.0.html; SLCC2; .NET CLR '
        '2.0.html.50727; .NET CLR 3.5.30729; .NET CLR 3.0.html.30729; Media Center PC 6.0.html; .NET4.0C; .NET4.0E; '
        'QQBrowser/7.0.html.3698.400)',
        # 搜狗浏览器
        'Mozilla/5.0.html (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.html.963.84'
        'Safari/535.11 SE 2.X MetaSr 1.0.html',
        # 360浏览器
        'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.html.1599.101 '
        'Safari/537.36',
        'Mozilla/5.0.html (Windows NT 6.1; WOW64; Trident/7.0.html; rv:11.0.html) like Gecko',
        # uc浏览器
        'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.html.2125.122 '
        'UBrowser/4.0.html.3214.0.html Safari/537.36',
        # 移动端的user-agen
        # IPhone
        'Mozilla/5.0.html (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, '
        'like Gecko) Version/5.0.html.2 Mobile/8J2 Safari/6533.18.5',
        # IPAD
        'Mozilla/5.0.html (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) '
        'Version/5.0.html.2 Mobile/8C148 Safari/6533.18.5',
        'Mozilla/5.0.html (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko)'
        'Version/5.0.html.2 Mobile/8J2 Safari/6533.18.5',
        # Android
        'Mozilla/5.0.html (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML,'
        'like Gecko) Version/4.0.html Mobile Safari/533.1',
        'Mozilla/5.0.html (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, '
        'like Gecko) Version/4.0.html Mobile Safari/533.1',
        # QQ浏览器 Android版本
        'MQQBrowser/26 Mozilla/5.0.html (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) '
        'AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0.html Mobile Safari/533.1',
        # Android Opera Mobile
        'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
        # Android Pad Moto Xoom
        'Mozilla/5.0.html (Linux; U; Android 3.0.html; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, '
        'like Gecko) Version/4.0.html Safari/534.13',
    ]
    headers = {
        'User-Agent': f'{choice(header_list)}'
    }
    return headers

# 网页美丽汤获取函数
def get_soup(url):
    res = get(url=url, headers=headers_random())
    sleep(5)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')
    return soup

# 网络文件的二进制数据获取函数
def get_data(url):
    res = get(url=url, headers=headers_random()).content
    sleep(5)
    return res

# 写文件函数
def write_file(file_path, mode, data, encoding='utf-8'):
    with open(file=file_path, mode=mode, encoding=encoding) as f:
        f.write(data)

# 写图像函数
def Write_pic(pic_path, data, mode='wb'):
    with open(file=pic_path, mode=mode, data=data) as p:
        p.write(data)

# Edge_driver
def Edge_driver(url):
    driver = webdriver.Edge()
    driver.implicitly_wait(30)
    driver.get(url=url)
    return driver

# Chrome_driver
def Chrome_driver(url):
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.get(url)
    return driver

# Firefox_driver
def Firefox_driver(url):
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(url)
    return driver

# 定时运行函数
def wait_time(hour, min):
    while tm().tm_hour <= int(hour) and tm().tm_min < (int(min) - 3):
        sleep(120)
    while tm().tm_hour == int(hour) and tm().tm_min < int(min):
        sleep(1)