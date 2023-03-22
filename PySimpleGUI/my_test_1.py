import PySimpleGUI as sg
import os

def users_window():
    layout = [
        [sg.Text('账号：'),sg.Input(key='Id')],
        [sg.Text('密码：'),sg.Input(key='passwd')],
        [sg.Button('GO'), sg.Button('Exit')]
    ]
    window = sg.Window(title='账号修改', layout=layout, size=[360, 100])
    event, valuse = window.read()
    if event not in (None, 'Exit'):
        window.close()
        sg.popup(f'{valuse}', title='users_dict')
        return valuse
    else:
        window.close()
        return None

def data_window():
    layout = [

    ]
    window = sg.Window(title='预约信息修改', layout=layout)
    event, valuse = window.read()
    if event not in (None, 'Exit'):
        return valuse
    else:
        return None
    
def home_wimdow():
    f = open('./seatId_dict.txt', 'r', encoding='utf-8')
    seatId_dict = eval(f.read())
    l = [1, 2, 3]
    layout = [sg.List()]
    window = sg.Window(title='预约信息修改', layout=layout)
    event, valuse = window.read()
    if event not in (None, 'Exit'):
        return valuse
    else:
        return None

if __name__ == '__main__':
    users = users_window()
    # home_wimdow()