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
users = ['2019*****', '******']  # 账密列表
homes = ['二楼社科借阅室(2)', '二楼社科借阅室(2)', '二楼社科借阅室(2)', '二楼社科借阅室(2)', '二楼社科借阅室(2)']  # 房间列表
seats = ['37', '38', '39', '40', '41']  # 座位列表
choice_date = 1
if tm().tm_hour == 21:  # 21点+运行则选择次日，否则默认为当日
    choice_date = 2


# 2.创建浏览器对象并打开目标网站：
print('打开登录界面...')
driver = webdriver.Chrome()   # 创建Edge浏览器对象
driver.implicitly_wait(30)  # 隐式等待
driver.get('https://cas.yangtzeu.edu.cn/authserver/login?service=https%3A%2F%2Fseat.yangtzeu.edu.cn%2Fremote%2Fstatic%2FcasAuth%2FgetServiceByVerifyTicket%2FcasLogin')

# 3.找到账号和密码的输入框，输入账号、密码并提交：
print('登录...')
driver.find_element('id', value='username').send_keys(users[0])  # 找到账号输入框并输入
driver.find_element('id', value='password').send_keys(users[1])  # 找到密码输入框并输入
submit_button = driver.find_element('id', value='login_submit').click()  # 提交
time.sleep(3)  # 等待3秒，避免页面还没加载完

# 4.进入预选界面并等待：
print('等待...')
driver.find_element('xpath', value='//a[@href="/libseat-ibeacon/activitySeat"]').click()  # 点击预约选座
while tm().tm_hour == 21 and tm().tm_min <= 37:  # 21:37以前每两分钟刷新一次
    time.sleep(120)
    driver.find_element('xpath', value='//a[@href="/libseat-ibeacon/activitySeat"]').click()  # 点击预约选座刷新
while tm().tm_hour == 21 and tm().tm_min < 40:  # 等待21:40准点继续运行
    time.sleep(1)

# 5.尝试选座
print('尝试选座...')
for home, seat in zip(homes, seats):

    global home_name
    home_name = home
    home_index = int(home_list.index(home))  # 获取房间位置
    seat_num = str('%03d' % int(seat))  # 格式化座位号

    for i in range(1, 11):  # 尝试选择日期循环

        driver.find_element('xpath', value='//a[@href="/libseat-ibeacon/activitySeat"]').click()  # 点击预约选座刷新

        try:
            driver.find_element('xpath', value=f'/html/body/div[1]/div[3]/div[{choice_date}]').click()  # 选择日期, 成功则进入下一步
        except Exception as d:
            print(f'选择日期第{i}次失败....')  # 输出选择日期失败提示

            if i != 10:
                with open('./exception.txt', 'w', encoding='utf-8') as f:  # 出错则记录Error
                    f.write(str(d))
            else:
                home_name = None  # 失败十次，返回房间空值
                print('选择日期失败...')

            continue  # 选择日期失败，则直接进入下一轮循环
        
        if home_name != None:  # 选择日期成功，尝试进入房间循环

            time.sleep(1)  # 等待加载

            for h in range(1, 11):  # 尝试进入房间循环
                try:
                    home_button = driver.find_elements('xpath', value='//*[@id="rooms"]/div/div[3]')[home_index - 1]
                    driver.execute_script('arguments[0].click();', home_button)
                except Exception as E:
                    print(f'进入房间"{home}"第{h}次失败....')  # 输出失败提示

                    with open('./yangtzeu_lib.txt', 'w', encoding='utf-8') as html:
                        html.write(driver.page_source)

                    if h != 10:
                        with open('./exception.txt', 'w', encoding='utf-8') as f:  # 出错则记录Error并退出脚本
                            f.write(f'home_index:{home_index}' + '\n')
                            f.write(str(E))
                    else:
                        print(f'进入房间"{home}"失败...')
                        home_name = None
                        break  # 跳出进入房间循环
                    continue  # 进入房间失败，则直接进入下一轮循环
                break  # 选择日期成功，进入房间成功，跳出进入房间循环
        else:
            home_name = None
            break  # 选择日期失败，则跳出选择日期 循环
        break  # 选择日期成功，进入房间成功，跳出选择日期循环
    
    if home_name != None:
        # 进入房间成功，尝试选择座位
        if 'green' in driver.find_element('xpath', value=f'//*[contains(span, {seat_num})]/img[1]').get_attribute('src'):  # 判断是否可选
            driver.find_element('xpath', value=f'//*[contains(span, {seat_num})]/img[1]').click()  # 选择座位号
            home_name = driver.find_element('xpath', value='//*[@id="timeSelete"]/div/div[1]/div[1]').text  # 预约房间名
            seat_numb = driver.find_element('xpath', value='//*[@id="timeSelete"]/div/div[1]/div[2]').text  # 预约座位号
            star_time_submit = driver.find_elements('xpath', value='//*[@id="start0"]/option')[0]  # 找到开始时间
            star_time = star_time_submit.text  # 获取开始时间
            star_time_submit.click()  # 选择开始时间
            end_time_submit = driver.find_elements('xpath', value='//*[@id="end0"]/option')[-1]  # 找到结束时间
            end_time = end_time_submit.text  # 获取结束时间
            star_time_submit.click()  # 选择结束时间
            driver.find_element('xpath', value=f'//*[@id="timeSelete"]/div/div[2]/button[1]').click()  # 点击确定
            break  # 选座成功，退出选座
        else:
            try:
                # 判断备选方案是否同一房间，不同则后退
                print(f'尝试备选方案{seats.index(seat) + 1}...')
                if homes[seats.index(seat) + 1] != homes[seats.index(seat)]:
                    driver.back()  # 后退
            except Exception as d:
                with open('./exception.txt', 'w+', encoding='utf-8') as f:  # 出错则记录Error并退出脚本
                    f.write(str(d))
                    print('查询完毕,但依然未预约成功...')
                    home_name = None
                    break
    else:  # 进入房间失败，则返回房间空值
        home_name = None
        break

# 6. 关闭浏览器并输出预约结果
driver.quit()
print('-' * 50)
print('我的学号：', users[0])
if 'seat_numb' in dir():
    print(home_name)
    print('预约座位号：', seat_numb)
    print('预约开始时间：', star_time)
    print('预约结束时间：', end_time)
else:
    print('未预约成功！！！')
print('-' * 50)
