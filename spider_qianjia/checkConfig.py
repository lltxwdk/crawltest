import configparser
import logging

# 获取配置
cfg = configparser.ConfigParser()
cfg.read("config.ini",'gbk')

class Config:

    def __init__(self):

        self.config = cfg
        #sys
        self.max_queue_len = int(self.config.get("sys", "max_queue_len"))
        self.crwaling_page = int(self.config.get("sys", "crwaling_page"))
        self.threads_num = int(self.config.get("sys", "thread_num"))
        #db
        self.db_host = self.config.get("db", "host")
        self.db_port = self.config.get("db", "port")
        self.db_user = self.config.get("db", "user")
        self.db_pass = self.config.get("db", "password")
        self.db_db = self.config.get("db", "db")
        self.db_charset = self.config.get("db", "charset")
        self.db_maxoverflow = int(self.config.get("db", "maxoverflow"))
        #redis
        self.redis_host = self.config.get("redis", "host")
        self.redis_port = self.config.get("redis", "port")
        #log
        self.level = int(self.config.get("log","level"))
        self.logname = self.config.get("log","logname")
        self.isfile = bool(self.config.get("log","file"))

    def GetSysConfigPara(self):
        sysConfDictory = {'ax_queue_len':self.max_queue_len,'threads_num':self.threads_num,'crwaling_page':self.crwaling_page}
        return sysConfDictory

    def GetRedisConfigPara(self):
        redisConfDictory={'redis_host':self.redis_host,'redis_port':self.redis_port}
        return redisConfDictory

    def GetDBConfigPara(self):
        dbConfDictory={'db_host':self.db_host,'db_port':self.db_port,'db_user':self.db_user,'db_pass':self.db_pass,'db_db':self.db_db,'db_charset':self.db_charset,'db_maxoverflow':self.db_maxoverflow}
        return dbConfDictory

    def GetLogConfigPara(self):
        logConfDictory = {'level':self.level,'logname':self.logname,'isfile':self.isfile}
        return logConfDictory
    
