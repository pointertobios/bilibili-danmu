#! /usr/bin/python

import threading
import time
import requests
import multiprocessing as proc
import tkinter

# 直播间号码
room_id = 24357339


MAX_MSGS = 12


def damuku(msg):
    global MAX_MSGS
    tk = tkinter.Tk()
    tk.wm_attributes('-topmost', 1)
    tk.overrideredirect(True)
    lb = tkinter.Label(tk, text=msg, height=1, bd=0, font=('文泉驿微米黑', 12, ''))
    lb.pack()
    tk.update()
    x = tk.winfo_screenwidth()
    y = tk.winfo_screenheight() - tk.winfo_height()
    for _ in range(tk.winfo_width()):
        x -= 1
        tk.geometry("+{}+{}".format(x, y))
        tk.update()
        time.sleep(0.0002)
    for i in range(MAX_MSGS):
        while not sigs[i]:
            pass
        sigs[i] = False
        for _ in range(40):
            y -= 1
            tk.geometry("+{}+{}".format(x, y))
            tk.update()
            time.sleep(0.005)


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
        self.log_file_write = open(
            '/home/pointer-to-bios/danmu.log', mode='a', encoding='utf-8')
        # 读取日志
        log_file_read = open(
            '/home/pointer-to-bios/danmu.log', mode='r', encoding='utf-8')
        self.log = log_file_read.readlines()

    def get_danmu(self):
        global MAX_MSGS
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
                # 保存日志
                self.log_file_write.write(msg + '\n')
                # 添加到日志列表
                self.log.append(msg + '\n')
                # 显示消息(msg)
                # 在此插入显示消息代码
                process = proc.Process(target=damuku, args=(msg,))
                for i in range(msgcount.value):
                    sigs[i] = True
                for i in range(msgcount.value):
                    while sigs[i]:
                        pass
                msgcount.value += 1
                if msgcount.value > MAX_MSGS:
                    msgcount.value = MAX_MSGS
                process.start()
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
            time.sleep(0.01)


if __name__ == "__main__":
    msgcount = proc.Value('i', 0)
    sigs = proc.Array('i', [0 for _ in range(MAX_MSGS)])
    thr = BilibiliThread(room_id)
    thr.start()
