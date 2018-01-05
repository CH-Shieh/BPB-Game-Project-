import sqlite3
import datetime

class DB:

    default_data = [
    ["Buuble", "15000", "20"],
    ["Buuble", "12500", "15"],
    ["Buuble", "10000", "10"],
    ["Buuble", "7500", "8"],
    ["Buuble", "5000", "6"],
    ]
    #初始化--------------------------------------------------------------------------------------------------------------
    def __init__(self):
        global con, cur#建立資料庫連結
        con = sqlite3.connect('GameData.db')
        cur = con.cursor()#建立cursor物件
        cur.execute('''CREATE TABLE IF NOT EXISTS member (
            mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT, score INTEGER, combo INTEGER, time TEXT, sync TEXT)''')
        con.commit()#发送命令

        cur.execute("SELECT * FROM member ")#读取所有资料
        scores = cur.fetchall()
        if (len(scores) == 0):
            self.load_default()
            
    #写入(名字，分数）---------------------------------------------------------------------------------------------------
    def write(self,name=" ",score=0, maxcombo = 0, sync = "N"):
        
        now = datetime.datetime.now()#time
        w_time=now.strftime('%Y-%m-%d %H:%M:%S') #time-str
        #print(w_time)
        cur.execute("INSERT INTO member (name, score, combo, time, sync) VALUES(?, ?, ?, ?, ?)",(name , score, maxcombo, w_time, sync))
        con.commit()#发送命令

    #读取----------------------------------------------------------------------------------------------------------------
    def read(self):
        #results = cur.execute("SELECT * FROM member ")#读取所有资料
        cur.execute("SELECT * FROM member ORDER BY time DESC ")#读取所有资料，以分数排序
        scores = cur.fetchall()

        return scores

    #清除所有------------------------------------------------------------------------------------------------------------
    def deleteall(self):
        cur.execute(" DROP TABLE member ")#删除资料库
        
        cur.execute('''CREATE TABLE IF NOT EXISTS member (
            mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT, score INTEGER, combo INTEGER, time TEXT, sync TEXT)''')
        con.commit()#发送命令
        
    #內建成績------------------------------------------------------------------------------------------------------------
    def load_default(self):
        now = datetime.datetime.now()#time
        w_time=now.strftime('%Y-%m-%d %H:%M:%S') #time-str
        for data in self.default_data:
            cur.execute("INSERT INTO member (name, score, combo, time, sync) VALUES(?, ?, ?, ?, ?)",(data[0] , data[1], data[2], w_time, "N"))
            con.commit()#发送命令
