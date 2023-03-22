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

login_url = 'https://cas.yangtzeu.edu.cn/authserver/login?service=https%3A%2F%2Fseat.yangtzeu.edu.cn%2Fremote%2Fstatic%2FcasAuth%2FgetServiceByVerifyTicket%2FcasLogin'

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
            data = driver.page_source
            with open(f'./{home}.txt', 'w+', encoding='utf-8') as f:
                f.write(data)
                time.sleep(5)
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

if __name__ == '__main__':
    driver = login_in(url=login_url, users=users)
    for home in home_list[1:]:
        refresh_submit = driver.find_element('xpath', value='//a[@href="/libseat-ibeacon/activitySeat"]')  # 找到预约选座
        driver = try_click(driver=driver, submit=refresh_submit)  # 刷新
        into_room(driver=driver, home=home)