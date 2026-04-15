#!/usr/bin/env python3
import os
import pymysql
import sys
import psutil
import logging
import configparser
confile_log=os.path.expanduser("~/bin/config.ini")
config=configparser.ConfigParser()
try:
    config.read(confile_log)
    db_config={
            'host':config.get('database','host'),
            'user':config.get('database','user'),
            'password':config.get('database','password'),
            'database':config.get('database','database'),
            'charset':config.get('database','charset')
            }
    server_id=config.getint('monitor','server_id')
    log_file=os.path.expanduser(config.get('monitor','log_file'))
except Exception as e:
    print(e)
    sys.exit(1)




logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
            ]
        )
logger=logging.getLogger("CpuMonitor")
server_id=1
class CpuMonitor:
    def __init__(self,server_id,db_config):
        self.server_id=server_id
        self.db_config=db_config
        self.connection=None
        self.cursor=None
        logger.info(f"the first server_id is {server_id}")
    def get_cpu_usage(self):
        try:
            usage=psutil.cpu_percent(interval=1)
            logger.info(f"{usage}")
            return usage
        except Exception as e:
            logger.error(e)
    def insert_record(self,cpu_usage):
        try:
            self.connection=pymysql.connect(**self.db_config)
            self.cursor=self.connection.cursor()
            sql="insert into cpu_history(server_id,timestamp,cpu_usage) values(%s,NOW(),%s)"
            self.cursor.execute(sql,(self.server_id,cpu_usage))
            self.connection.commit()
            logger.info(f"成功插入记录: server_id={self.server_id}, cpu_usage={cpu_usage}%")
        except Exception as e:
            logger.error(e)
            if self.connection:
                self.connection.rollback()
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
    def run(self):
        usage=self.get_cpu_usage()
        self.insert_record(usage)
def main():
    monitor=CpuMonitor(server_id,db_config)
    monitor.run()
if __name__=="__main__":
    main()
