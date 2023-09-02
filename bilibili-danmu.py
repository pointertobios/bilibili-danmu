#! /usr/bin/python

import threading
import time
import requests
import multiprocessing as proc
import tkinter

# 直播间号码
room_id = 24357339


def damuku(msg):
    tk = tkinter.Tk()
    tk.wm_attributes('-topmost', 1)
    tk.overrideredirect(True)
    lb = tkinter.Label(tk, text=msg, height=1, bd=0, font=('文泉驿微米黑', 12, ''))
    lb.pack()
    pos = 0
    # while lock.value == True:
    #     time.sleep(0.001)
    # lock.value = True
    for i in range(len(posrec)):
        if posrec[i] == False:
            pos = i
            posrec[i] = True
            break
    # lock.value = False
    for i in range(tk.winfo_screenwidth(), 0, -1):
        if tk.winfo_screenwidth() - i == tk.winfo_width():
            posrec[pos] = False
        tk.geometry('+{}+{}'.format(i, pos * 40))
        tk.update()
        time.sleep(0.00833333333)


running = True


# B站获取弹幕对象
class Danmu():
    def __init__(self, room_id):
        # 弹幕url
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
        # 请求头
        self.headers = {
            'Host': 'api.live.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
        }
        # 定义POST传递的参数
        self.data = {
            'roomid': room_id,
            'csrf_token': '',
            'csrf': '',
            'visit_id': '',
        }
        # 日志写对象
        self.log_file_write = open('/home/pointer-to-bios/danmu.log', mode='a', encoding='utf-8')
        # 读取日志
        log_file_read = open('/home/pointer-to-bios/danmu.log', mode='r', encoding='utf-8')
        self.log = log_file_read.readlines()

    def get_danmu(self):
        # 获取直播间弹幕
        while True:
            try:
                html = requests.post(
                    url=self.url, headers=self.headers, data=self.data).json()
                break
            except requests.exceptions.RequestException:
                continue
        # 解析弹幕列表
        for content in html['data']['room']:
            # 获取昵称
            nickname = content['nickname']
            # 获取发言
            text = content['text']
            # 获取发言时间 HH:mm:ss
            timeline = content['timeline'].split(" ")[1]
            # 记录发言
            msg = timeline + ' ' + nickname + ': ' + text
            # 判断对应消息是否存在于日志，如果和最后一条相同则打印并保存
            if msg + '\n' not in self.log:
                # 显示消息(msg)
                # 在此插入显示消息代码
                process = proc.Process(target=damuku, args=(msg,))
                process.start()
                # 保存日志
                self.log_file_write.write(msg + '\n')
                # 添加到日志列表
                self.log.append(msg + '\n')
            # 清空变量缓存
            nickname = ''
            text = ''
            timeline = ''
            msg = ''


# 线程对象
def bilibili(room_id):
    # 创建bDanmu实例
    bDanmu = Danmu(room_id)
    # 获取弹幕
    bDanmu.get_danmu()


class BilibiliThread(threading.Thread):
    def __init__(self, room_id=None):
        threading.Thread.__init__(self)
        self.room_id = room_id

    # 重写run()方法
    def run(self):
        global running
        while running:
            bilibili(self.room_id)
            time.sleep(0.5)


if __name__ == "__main__":
    posrec = proc.Array('i', [False for _ in range(int(900 / 40))])
    lock = proc.Value('d', False)
    thr = BilibiliThread(room_id)
    thr.start()
