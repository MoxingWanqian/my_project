import time

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

seatId_dict = dict()

for home in home_list[1:]:
    with open(f'./{home}.txt', 'r', encoding = 'utf-8') as f:
        datas = f.readlines()
        seatId_dict[datas[0].replace('\n', '')] = dict()
        for data in datas[1:]:
            data = data.replace('\n', '').split(', ')
            seatId_dict[datas[0].replace('\n', '')][data[0]] = data[1]
with open('./seatId_dict.txt', 'w', encoding='utf-8') as d:
    d.write(str(seatId_dict))

