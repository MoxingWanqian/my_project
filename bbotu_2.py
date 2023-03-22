import time
import requests
from lxml import etree
from selenium import webdriver

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

def get_res(driver, url):
    cookies = driver.get_cookies()
    sess = requests.Session()
    for cookie in cookies:
        # print(cookie)
        sess.cookies.set(name=cookie['name'], value=cookie['value'])
    headers = {
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "referer": "https://www.bbotu.com/66/",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/53"
    }
    res = sess.get(url=url, headers=headers)
    res.encoding = res.apparent_encoding
    return res

def get_data(res):
    tree = etree.HTML(res.text)
    with open('./res.txt', 'w', encoding='utf-8') as f:
        f.write(res.text)
    data = tree.xpath('//div[@class="card-body"]//text()')
    return data

def main():
    driver = start_driver(url=home_url)
    driver = login_in(driver=driver)
    response = get_res(driver=driver, url=url)
    data = get_data(res=response)
    print(data) 
    driver.quit()

if __name__ == '__main__':
    url = 'https://www.bbotu.com/245/'
    home_url = 'https://www.bbotu.com'
    url_1 = 'https://www.bbotu.com/?s=%E7%9C%BC%E9%85%B1'
    main()
