import os
import time
import lackey
import keyboard
from pywinauto.application import Application

os.environ.update({"__COMPAT_LAYER": "RUnAslnvoker"})

# 运行原神程序
def start_YuanShen():
    YuanShen_exe = r'C:\Program Files\Genshin Impact\Genshin Impact Game\YuanShen.exe'
    app = Application(backend='uia').start(YuanShen_exe, timeout=120)
    time.sleep(5)
    lackey.wait(r'YuanShen\YuanShen_photos\YuanShen_login.png')
    return app

# 登录
def login_enter():
    time.sleep(5)
    lackey.wait(r'YuanShen\YuanShen_photos\YuanShen_login.png')
    if lackey.wait(r'YuanShen\YuanShen_photos\YuanShen_login.png'):
        lackey.click(r'YuanShen\YuanShen_photos\YuanShen_login.png')

# 打开地图，并前往蒙德初始位置
def go_to_MenDe():
    time.sleep(5)
    lackey.wait(r'YuanShen\YuanShen_photos\login_succeed.png')
    keyboard.send('m')
    lackey.wait(r'YuanShen\YuanShen_photos\map_marker.png')
    lackey.click(r'YuanShen\YuanShen_photos\map_marker.png')
    if lackey.wait(r'YuanShen\YuanShen_photos\MenDe_black.png') or lackey.wait(r'YuanShen\YuanShen_photos\LiYue_black.png'):
        try:
            lackey.click(r'YuanShen\YuanShen_photos\MenDe_black.png')
        except:
            lackey.click(r'YuanShen\YuanShen_photos\LiYue_black.png')
            time.sleep(2)
            lackey.click(r'YuanShen\YuanShen_photos\map_marker_of_DaoQi.png')
            lackey.click(r'YuanShen\YuanShen_photos\MenDe_black.png')
    lackey.wait(r'YuanShen\YuanShen_photos\map_of_wolf_king.png')
    lackey.click(r'YuanShen\YuanShen_photos\marker_of_MenDe_1.png')
    lackey.wait(r'YuanShen\YuanShen_photos\send_to.png')
    lackey.click(r'YuanShen\YuanShen_photos\send_to.png')
    

# 自动完成每日任务

# 自动合成浓缩树脂

# 前往蒙德合成台

# start_YuanShen()
login_enter()
# go_to_MenDe()