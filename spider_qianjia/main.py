import requests
import http.cookiejar as cookielib
import configparser
from bs4 import BeautifulSoup
import bs4
import sys
import json
import math
import traceback
import threading
import time
import random
from checkConfig import Config
from logger.log import LogHandler
from db.db import DataBase
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askdirectory
import os
postUrl = 'https://bsitefront.allhome.com.cn/v1/website/second/house/list'
payloadHeader = {
    'authority': 'bsitefront.allhome.com.cn',
    'method': 'POST',
    'path': '/v1/website/second/house/list',
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-length': '144',
    'content-type': 'application/json;charset=UTF-8',
    'dnt': '1',
    'origin': 'https://www.allqj.com',
    'referer': 'https://www.allqj.com/',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'terminal': 'web',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
class Interface():
    def __init__(self):
        self.window = tk.Tk()  #创建window窗口
        self.window.title("Crawler Pics")  # 定义窗口名称
        # self.window.resizable(0,0)  # 禁止调整窗口大小
        self.menu = ttk.Combobox(self.window,width=6)
        self.path = StringVar()
        self.lab1 = tk.Label(self.window, text = "目标路径:")
        self.lab2 = tk.Label(self.window, text="选择分类:")
        self.input = tk.Entry(self.window, textvariable = self.path, width=80)  # 创建一个输入框,显示图片存放路径
        self.info = tk.Text(self.window, height=50)   # 创建一个文本展示框，并设置尺寸

        self.menu['value'] = ('一居室','二居室', '三居室')
        self.menu.current(0)

        # 添加一个按钮，用于选择图片保存路径
        self.t_button = tk.Button(self.window, text='选择路径', relief=tk.RAISED, width=8, height=1, command=self.select_Path)
        # 添加一个按钮，用于触发爬取功能
        self.t_button1 = tk.Button(self.window, text='爬取', relief=tk.RAISED, width=8, height=1,command=self.download)
        # 添加一个按钮，用于触发清空输出框功能
        self.c_button2 = tk.Button(self.window, text='查询', relief=tk.RAISED,width=8, height=1, command=self.check)
        self.c_button3 = tk.Button(self.window, text='删除', relief=tk.RAISED,width=8, height=1, command=self.delete)
    def gui_arrang(self):
        """完成页面元素布局，设置各部件的位置"""
        self.lab1.grid(row=0,column=0)
        self.lab2.grid(row=1, column=0)
        self.menu.grid(row=1, column=1,sticky=W)
        self.input.grid(row=0,column=1)
        self.info.grid(row=3,rowspan=15,column=0,columnspan=3,padx=15,pady=15)
        self.t_button.grid(row=0,column=2,padx=5,pady=5,sticky=tk.W)
        self.t_button1.grid(row=0,column=3)
        self.c_button2.grid(row=1,column=2,padx=5,pady=5,sticky=tk.W)
        self.c_button3.grid(row=1,column=3,padx=5,pady=5,sticky=tk.W)
    def select_Path(self):
        """选取本地路径"""
        path_ = askdirectory()
        self.path.set(path_)
    def getTypeId(self):
        category = {
            'YJS': 1,
            'EJS': 2,
            'SJS': 3
        }
        cid = None
        if self.menu.get() == "一居室":
            cid = category["YJS"]
        elif self.menu.get() == "二居室":
            cid = category["EJS"]
        elif self.menu.get() == "三居室":
            cid = category["SJS"]
        return cid

    def download(self):
        #多线程
        for i in range(0, threads_num):
            m = Spider(i, "thread" + str(i),self.input.get())
            threads.append(m)

        for i in range(0, threads_num):
            threads[i].start()

        for i in range(0, threads_num):
            threads[i].join()

    def check(self):
        self.info.delete(1.0,"end")  # 从第一行清除到最后一行
        houseType = self.getTypeId()
        logs.debug("查询条件，房屋类型：code=%d",houseType)
        result = db.selectInfo(houseType)
        if len(result) > 0:
            for value in result:
                Title = "房屋编号："+ str(value.id) + "       名称："+value.title+'\n'
                self.info.insert('end',Title)
                Info = "房屋格局：" + value.houseType+"     社区："+value.community+'\n'
                self.info.insert('end',Info)
                Info = value.district+"-"+value.region+" / "+value.area+"平米/ "+value.direction+" / "+value.decoration+'\n'
                self.info.insert('end',Info)
                Info = str(value.topFloor)+"层 / " +value.builtYears+"年建成 / "+value.propertyAge+"年产权 / " + '\n'
                self.info.insert('end',Info)
                Price = "总售卖价格："+str(value.salePrice)+"万元" + " / 单价：" + str(value.unitPrice*1000) + "元/平米" + '\n'
                self.info.insert('end',Price)
                self.info.insert('end','\n')

        else:
            logs.debug("未查询到结果")
            self.info.insert('end','未查询到结果,设置条件重新查询')

    def delete(self):
        houseType = self.getTypeId()
        result = db.deleteInfo(houseType)
#多线程
class Spider(threading.Thread):

    def __init__(self, threadID=1, name='',filepath=''):
        # 多线程
        print("线程" + str(threadID) + "初始化")
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        try:
            print("线程" + str(threadID) + "初始化成功")
        except Exception as err:
            print(err)
            print("线程" + str(threadID) + "开启失败")

        self.threadLock = threading.Lock()
        self.filepath = filepath
        logs.debug(self.filepath)
    def get_image_content(self, url):
        """请求图片url，返回二进制内容"""
        logs.debug("正在下载%s", url)

        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.content
            return None
        except RequestException:
            return None

    def startGrabInfo(self,beginPage,endPage):
        for currentPage in range(beginPage+1,endPage+1):
            logs.debug("正在请求第%d页,线程:%s",currentPage,self.threadID)
            payloadData = {
                'pageInfo': {
                    'page': currentPage,
                    'size': 20,
                    'sortVO': [
                        {
                            'sort': "DESC",
                            'sortBy': "uSort"
                        },
                        {
                            'sort': "DESC",
                            'sortBy': "modifytime"
                        }
                    ]
                },
                'query': {
                    'communityName': ""
                },
            }
            try:
                res = requests.post(postUrl, json=payloadData, headers=payloadHeader)
                rcontext = res.text.split('data":[')[1].split(']},"statusCode')[0]
                for j in range(1, 21):
                    unite = rcontext.split('{')[j].split('}')[0]
                    unite = '{' + unite+ '}'
                    unite = json.loads(unite)
                    logs.debug("id:%s,title:%s,houseTypeCode:%d",unite['id'],unite['title'],unite['houseTypeCode'])
                    self.threadLock.acquire()
                    db.insert(unite['id'],unite['coverImageUrl'],unite['salePrice'],
                            unite['title'],unite['unitPrice'],unite['houseType'],
                            unite['area'],unite['direction'],unite['decoration'],
                            unite['houseTypeCode'],unite['community'],unite['floorLayer'],
                            unite['status'],unite['region'],unite['district'],
                            unite['topFloor'],unite['builtYears'],unite['propertyAge'])
                    self.threadLock.release()

                    root_dir = self.filepath
                    if not os.path.exists(root_dir + '/pics'):
                        os.makedirs(root_dir + '/pics')
                    if not os.path.exists(root_dir + '/pics/' + unite['id']):
                        os.makedirs(root_dir + '/pics/' + unite['id'])

                    saveFilePath = root_dir + '/pics/' + unite['id'] +'/'+ unite['id'] + '.jpg'
                    if not os.path.exists(saveFilePath):  # 判断是否存在文件，不存在则爬取
                            with open(saveFilePath, 'wb') as f:
                                f.write(self.get_image_content(unite['coverImageUrl']))
                                f.close()
                                logs.debug('文件保存成功')

            except Exception as e:
                logs.debug("失败：%s",str(e))
                failPageCount.append(currentPage)
        logs.debug(failPageCount)

    def entrance(self):
        logs.debug("线程总数：%d,当前线程:%s,",threads_num,self.threadID)
        if self.threadID % threads_num == threads_num-1:
            start = self.threadID*distributeNum
            end = page
            logs.debug("start:%d,end:%d",start,end)
            self.startGrabInfo(start,end)
        else:
            start = self.threadID*distributeNum
            end = start + distributeNum
            logs.debug("start:%d,end:%d",start,end)
            self.startGrabInfo(start,end)

    def run(self):
        logs.debug(self.name + " is running")
        self.entrance()

if __name__ == "__main__":
    threads = []
    #多线程
    config = Config()
    sysConfig = config.GetSysConfigPara()
    logConfig = config.GetLogConfigPara()
    dbConfig = config.GetDBConfigPara()
    logs = LogHandler(logConfig['logname'],logConfig['level'],logConfig['isfile'])
    db = DataBase(dbConfig['db_host'],dbConfig['db_port'],dbConfig['db_user'],dbConfig['db_pass'],dbConfig['db_db'],dbConfig['db_charset'],dbConfig['db_maxoverflow'])
    threads_num = sysConfig['threads_num']
    db.connectDB()
    page = sysConfig['crwaling_page']
    distributeNum = int(page / threads_num)
    failPageCount=[]
    logs.debug("distributeNum:%d",distributeNum)

    interface = Interface()
    interface.gui_arrang()
    tk.mainloop()
    
