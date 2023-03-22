# 1.导入所需库：
import time
import requests
from lxml import etree
from selenium import webdriver


#构造请求头
headers = {
    'User-Agent': 'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.html.2171.71 Safari/537.36'
}

# 创建浏览器对象并打开目标网站：
def start_driver(url):
    op = webdriver.EdgeOptions()
    op.add_argument('--headless')
    driver = webdriver.Edge()   # 创建浏览器对象
    driver.implicitly_wait(30)
    driver.get(url)
    return driver

# 找到账号和密码的输入框，输入账号、密码并提交：
def login_in(driver):
    driver.find_element('xpath', value='//a[@href="#"]').click()  # 点击“登录”按钮
    driver.find_element('name', value='username').send_keys('2995749773@qq.com')  # 找到账号输入框并输入
    driver.find_element('name', value='password').send_keys('20010212a')  # 找到密码输入框并输入
    driver.find_element('xpath', value='//form/div[@class="row"]/div[3]/button').click() #提交
    return driver

# # 获取cookies并退出
# cookies = driver.get_cookies()
# # driver.close()

# # 携带cookies访问详情页
# sess = requests.session()
# cookie = cookies[1]
# sess.cookies.set(name=cookie['name'], value=cookie['value'], domain='.bbotu.com', path='/', secure=False)
# # for cookie in cookies:
# #     print(cookie)
# #     sess.cookies.set(name=cookie['name'], value=cookie['value'], domain='.bbotu.com', path='/', httpOnly=cookie['httpOnly'], sameSite=cookie['sameSite'], secure=False)
# res = sess.get(url='https://www.bbotu.com/66/')
# res.encoding = res.apparent_encoding

# tree = etree.HTML(res.text)
# with open('./response.txt', 'w', encoding='utf-8') as f:
#     f.write(res.text)
# data = tree.xpath('//div[@class="card-body"]/div//text()')
# print(str(data))

# 输入搜索值并提交：
def search_keywd(driver, keywd):
    keywd_button = driver.find_element('xpath', value='//input[@type="text"]')  # 找到搜索输入框
    keywd_button.send_keys(keywd)  # 输入搜索关键词
    ok_submit = driver.find_element('xpath', value='//form/div[2]/button')
    ok_submit.click()  # 提交
    return driver

def select_first(driver):
    select_submit = driver.find_element('xpath', value='//header[@class="entry-header"]')
    select_submit.click()
    return driver

# 6.获取百度网盘链接及密码
# title = driver.title()
# print(title)
def get_data(driver):
    data = driver.find_element('xpath', value='//div[@class="card-body"]/div').text
    return data

def print_data(data):
    print(f'{data[0]}')
    print(f'{data[1]}')
    print(f'{data[2]}')

def main():
    driver = start_driver(url=home_url)
    driver = login_in(driver=driver)
    driver = search_keywd(driver=driver, keywd=keywd)
    driver = select_first(driver=driver)
    data = get_data(driver=driver)
    data = data.replace('提取码（点击复制）：', '\n').replace('解压码（点击复制）：', '\n').split('\n')
    print_data(data=data)

if __name__ == '__main__':
    keywd = '桜桃喵'
    home_url = 'https://www.bbotu.com'
    main()
    