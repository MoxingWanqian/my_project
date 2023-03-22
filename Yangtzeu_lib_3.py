# 1.导入所需库：
import time
import json
import requests
from selenium import webdriver
from time import localtime as tm

# 房间名列表
home_list = [
    '三楼自科借阅室(1)',
    '四楼大厅',
    '四楼自科借阅室(2)'
]

# 房间Id列表
roomsId = {
    '一楼社科借阅室(1)': 1,
    '一楼社科借阅室(3)': 2,
    '二楼社科借阅室(2)': 3,
    '二楼大厅': 4,
    '二楼报刊阅览室(1)': 5,
    '二楼报刊阅览室(2)': 6,
    '三楼大厅': 8,
    '三楼外文借阅室': 9,
    '一楼电子文献阅览室': 13
}

# 个人信息与预约信息字典
users = {'Id': '201904893', 'passwd': 'Yangtzeu2019@Liu'}  # 账密字典
data_dict = {'roomId': roomsId['二楼社科借阅室(2)'], 'seatId': 1329, 'start_time': 7, 'end_time': 21}

login_url = 'https://cas.yangtzeu.edu.cn/authserver/login?service=https%3A%2F%2Fseat.yangtzeu.edu.cn%2Fremote%2Fstatic%2FcasAuth%2FgetServiceByVerifyTicket%2FcasLogin'

# 填写日期
def choice_date():
    if tm().tm_hour >= 21:  # 21点+运行则选择次日，否则默认为当日
        date_num = tm().tm_mday + 1
    else:
        date_num = tm().tm_mday
    return date_num

# 创建浏览器对象并打开目标网站：
def start_driver(url):
    print('打开登录界面...')
    driver = webdriver.Edge()   # 创建Edge浏览器对象
    driver.implicitly_wait(30)  # 隐式等待
    driver.get(url)
    return driver

# 找到账号和密码的输入框，输入账号、密码并提交：
def input_Account(driver, users):
    print('登录...')
    driver.find_element('id', value='username').send_keys(users['Id'])  # 找到账号输入框并输入
    driver.find_element('id', value='password').send_keys(users['passwd'])  # 找到密码输入框并输入
    driver.find_element('id', value='login_submit').click()  # 提交
    time.sleep(3)  # 等待3秒，避免页面还没加载完
    return driver

# 登录
def login_in(url, users):
    driver = start_driver(url=url)
    driver = input_Account(driver=driver, users=users)
    return driver

# 进入预选界面并等待：
def wait_time(driver):
    print('等待...')
    while tm().tm_hour == 21 and tm().tm_min <= 37:  # 21:37以前每两分钟刷新一次
        time.sleep(120)
        refresh_submit = driver.find_element('xpath', value='//a[@href="/libseat-ibeacon/activitySeat"]')  # 找到预约选座
        driver = try_click(driver=driver, submit=refresh_submit)  # 刷新
    while tm().tm_hour == 21 and tm().tm_min < 39:  # 等待21:40准点继续运行
        time.sleep(1)
    refresh_submit = driver.find_element('xpath', value='//a[@href="/libseat-ibeacon/activitySeat"]')  # 找到预约选座
    driver = try_click(driver=driver, submit=refresh_submit)  # 刷新
    return driver

# 计算时间Id
def get_time(start_time, end_time):
    start_time_hour = int(start_time)
    end_time_hour = int(end_time)
    if (float(start_time) - start_time_hour) == 0:
        start_num = start_time_hour * 60
    else:
        start_num = start_time_hour * 60 + 30
    if (float(end_time) - end_time_hour) == 0:
        end_num = end_time_hour * 60
    else:
        end_num = end_time_hour * 60 + 30
    return start_num, end_num

# 获取cookies
def get_seat(driver, roomId, seatId, start_num, end_num, date_num=tm().tm_mday):
    year = tm().tm_year
    month = '%02d' % tm().tm_mon
    cookies = driver.get_cookies()
    sess = requests.Session()
    for cookie in cookies:
        sess.cookies.set(name=cookie['name'], value=cookie['value'])
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Host": "seat.yangtzeu.edu.cn",
        "Referer": f"http://seat.yangtzeu.edu.cn/libseat-ibeacon/seatdetail?linkSign=activitySeat&roomId={roomId}&date={year}-{month}-{date_num}&buildId=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
        "X-Requested-With": "XMLHttpRequest"
    }
    while tm().tm_hour == 21 and tm().tm_min < 40:
        time.sleep(1)
    for i in range(10):
        try:
            res = sess.get(url=f'http://seat.yangtzeu.edu.cn/libseat-ibeacon/saveBook?seatId={seatId}&date={year}-{month}-{date_num}&start={start_num}&end={end_num}&type=1&captchaToken=', headers=headers)
        except:
            continue
        res.encoding = res.apparent_encoding
        res = res.text.replace('\\', '')
        num = len(res) - 1
        res = res[1:num]
        res = json.loads(res)
        status = res['status']
        if status == 'success':
            data = res['data']
            onDate = data['onDate']
            begin = data['begin']
            end = data['end']
            location = data['location']
            break
        else:
            end_num -= 30
            continue
    return status, onDate, begin, end, location

# 尝试点击
def try_click(driver, submit):
    try:
        submit.click()
    except:
        try:
            driver.execute_script('arguments[0].click();', submit)
        except:
            print(f'尝试点击"{submit}"出错...')
    return driver

# 结果输出函数
def print_result(users, status, onDate, begin, end, location):
    print('-' * 50)
    print('Id: ', users['Id'])
    if status == 'success':
        print('onDate: ', onDate)
        print('location:', location)
        print('begin: ', begin)
        print('end: ', end)
    else:
        print('Feiled!!!')
    print('-' * 50)

# 主函数
def main():
    date_num = choice_date()
    driver = login_in(url=login_url, users=users)
    start_num, end_num = get_time(start_time=data_dict['start_time'], end_time=data_dict['end_time'])
    driver = wait_time(driver=driver)
    status, onDate, begin, end, location = get_seat(driver=driver, roomId=data_dict['roomId'], seatId=data_dict['seatId'], start_num=start_num, end_num=end_num, date_num=date_num)
    print_result(users, status, onDate, begin, end, location)
    time.sleep(10)


# 主程序入口
if __name__ == '__main__':
    main()