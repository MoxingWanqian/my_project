# 1.导入所需库：
import time
from selenium import webdriver
from time import localtime as tm

# 房间名列表
home_list = [
    '',
    '一楼电子文献阅览室',
    '一楼社科借阅室(1)',
    '一楼社科借阅室(3)',
    '二楼大厅',
    '二楼报刊阅览室(1)',
    '二楼报刊阅览室(2)',
    '二楼社科借阅室(2)',
    '三楼外文借阅室',
    '三楼大厅',
    '三楼自科借阅室(1)',
    '四楼大厅',
    '四楼自科借阅室(2)'
]

# 房间名需与座位号一一对应
users = ['201904893', 'Yangtzeu2019@Liu']  # 账密列表
homes = ['二楼社科借阅室(2)', '二楼社科借阅室(2)', '二楼社科借阅室(2)', '二楼社科借阅室(2)', '二楼社科借阅室(2)']  # 房间列表
seats = ['37', '38', '39', '40', '41']  # 座位号列表

login_url = 'https://cas.yangtzeu.edu.cn/authserver/login?service=https%3A%2F%2Fseat.yangtzeu.edu.cn%2Fremote%2Fstatic%2FcasAuth%2FgetServiceByVerifyTicket%2FcasLogin'

# 填写日期
def choice_date(date_num=1):
    if tm().tm_hour >= 21:  # 21点+运行则选择次日，否则默认为当日
        date_num = 2
    return date_num

# 创建浏览器对象并打开目标网站：
def start_driver(url):
    print('打开登录界面...')
    driver = webdriver.Chrome()   # 创建Edge浏览器对象
    driver.implicitly_wait(30)  # 隐式等待
    driver.get(url)
    return driver

# 找到账号和密码的输入框，输入账号、密码并提交：
def input_Account(driver, users):
    print('登录...')
    driver.find_element('id', value='username').send_keys(users[0])  # 找到账号输入框并输入
    driver.find_element('id', value='password').send_keys(users[1])  # 找到密码输入框并输入
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
    while tm().tm_hour == 21 and tm().tm_min < 40:  # 等待21:40准点继续运行
        time.sleep(1)
    return driver

# 选择日期
def choose_date(driver, date_num=1):
    print('选择日期...')
    for i in range(1, 11):  # 尝试选择日期循环
        refresh_submit = driver.find_element('xpath', value='//a[@href="/libseat-ibeacon/activitySeat"]')  # 找到预约选座
        driver = try_click(driver=driver, submit=refresh_submit)  # 刷新
        try:
            date_submit = driver.find_element('xpath', value=f'/html/body/div[1]/div[3]/div[{date_num}]')  # 找到日期
            driver = try_click(driver=driver, submit=date_submit)  # 选择日期
            print('选择日期成功...')
            break
        except Exception as d:
            print(f'选择日期第{i}次失败....')  # 输出选择日期失败提示
            if i != 10:
                continue
            else:
                with open('./exception.txt', 'w', encoding='utf-8') as f:  # 出错则记录Error
                    f.write(str(d))
                print('选择日期失败...')
                break
    return driver


# 进入房间
def into_room(driver, home):
    print(f'进入房间"{home}"...')
    home_index = home_list.index(home)
    for h in range(1, 11):  # 尝试进入房间循环
        try:
            print(f'尝试进入房间"{home}"第{h}次...')
            home_button = driver.find_elements('xpath', value='//*[@id="rooms"]/div/div[3]')[home_index - 1]
            driver = try_click(driver, home_button)
            print(f'尝试进入房间"{home}"成功...')
            break
        except Exception as E:
            print(f'进入房间"{home}"第{h}次失败....')  # 输出失败提示
            with open('./yangtzeu_lib.txt', 'w', encoding='utf-8') as html:
                html.write(driver.page_source)
            if h != 10:
                with open('./exception.txt', 'w', encoding='utf-8') as f:  # 出错则记录Error并退出脚本
                    f.write(f'home_index:{home_index}' + '\n')
                    f.write(str(E))
                    continue  # 进入房间失败，则直接进入下一轮循环
            else:
                print(f'进入房间"{home}"失败...')
    return driver


# 选座
def get_seat(driver, seat):
    print('选座...')
    seat_num = str('%03d' % int(seat))  # 格式化座位号
    if 'green' in driver.find_element('xpath', value=f'//*[contains(span, {seat_num})]/img[1]').get_attribute('src'):  # 判断是否可选
        seat_submit = driver.find_element('xpath', value=f'//*[contains(span, {seat_num})]/img[1]')  # 招到座位号
        driver = try_click(driver, seat_submit)  # 点击座位号
        home_name = driver.find_element('xpath', value='//*[@id="timeSelete"]/div/div[1]/div[1]').text  # 预约房间名
        seat_numb = driver.find_element('xpath', value='//*[@id="timeSelete"]/div/div[1]/div[2]').text  # 预约座位号
        star_time_submit = driver.find_elements('xpath', value='//*[@id="start0"]/option')[0]  # 找到开始时间
        star_time = star_time_submit.text  # 获取开始时间
        driver = try_click(driver, star_time_submit)  # 选择开始时间
        time.sleep(0.5)
        end_time_submit = driver.find_elements('xpath', value='//*[@id="end0"]/option')[-1]  # 找到结束时间
        end_time = end_time_submit.text  # 获取结束时间
        driver = try_click(driver, end_time_submit)  # 选择结束时间
        ok_submit = driver.find_element('xpath', value=f'//*[@id="timeSelete"]/div/div[2]/button[1]')  # 找到确定按钮
        driver = try_click(driver, ok_submit)  # 点击确定
    return driver, home_name, seat_numb, star_time, end_time

# 尝试选座
def get_lib_seat(driver, date_num=1):
    print('尝试选座...')
    for home, seat in zip(homes, seats):
        home_name = home
        seat_numb = 0
        star_time = 0
        end_time = 0
        try:
            driver = choose_date(driver=driver, date_num=date_num)
            driver, home_name = into_room(driver=driver, home=home)
            driver, home_name, seat_numb, star_time, end_time = get_seat(driver=driver, seat=seat)
            break
        except:  # 进入房间失败，则继续循环
            continue
    return home_name, seat_numb, star_time, end_time

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
def print_result(users, home_name, seat_numb, star_time, end_time):
    print('-' * 50)
    print('我的学号：', users[0])
    if seat_numb != 0:
        print(home_name)
        print('预约座位号：', seat_numb)
        print('预约开始时间：', star_time)
        print('预约结束时间：', end_time)
    else:
        print('未预约成功！！！')
    print('-' * 50)

# 主函数
def main():
    date_num = choice_date(date_num=1)
    driver = login_in(url=login_url, users=users)
    driver = wait_time(driver=driver)
    home_name, seat_numb, star_time, end_time = get_lib_seat(driver=driver, date_num=date_num)
    print_result(users=users, home_name=home_name, seat_numb=seat_numb, star_time=star_time, end_time=end_time) 

# 主程序入口
if __name__ == '__main__':
    main()