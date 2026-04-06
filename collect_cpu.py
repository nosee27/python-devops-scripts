#!/usr/bin/env python3
import os
import logging
import json
import pymysql
import sys
import psutil
from datetime import datetime
LOG_FILE=os.path.expanduser("~/cpu_monitor.log")
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
        ]
)
logger=logging.getLogger("CpuMonitor")

db_config={
        'host':'localhost',
        'user':'root',
        'password':os.environ.get('MYSQL_PASSWORD','Yang228056@'),
        'password':os.environ.get('MySQL_PASSWORD','password'),
        'database':'devops',
        'charset':'utf8mb4'
        }
server_id=1

class CpuMonitor:
    def __init__(self,server_id,db_config):
        self.server_id=server_id
        self.db_config=db_config
        self.connection=None
        self.cursor=None
        logger.info(f"server_id+{self.server_id}")
    def get_cpu_usage(self,interval=1):
        try:
            usage=psutil.cpu_percent(interval=interval)
            logger.debug(f"get{usage}%")
            return usage
        except Exception as e:
            logger.error(f"wrong{e}")
            raise
    def connect_db(self):
        try:
            self.connection=pymysql.connect(**self.db_config)
            self.cursor=self.connection.cursor()
            logger.debug("数据库连接成功")
        except Exception as e:
            logger.error(f"wrong{e}")
            raise
    def close_db(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    def insert_record(self,cpu_usage):
        try:
            self.connect_db()
            sql="insert into cpu_history(server_id,timestamp,cpu_usage) values (%s,NOW(),%s)"
            self.cursor.execute(sql,(self.server_id,cpu_usage))
            self.connection.commit()
            logger.info(f"成功插入记录: server_id={self.server_id}, cpu_usage={cpu_usage}%")
        except Exception as e:
            logger.error(f"wrong{e}")
            if self.connection:
                self.connection.rollback()
            raise
        finally:
            self.close_db()
    def run_once(self):
        try:
            cpu_usage=self.get_cpu_usage()
            self.insert_record(cpu_usage)
        except Exception as e:
            logger.error(f"执行失败: {e}", exc_info=True)
            sys.exit(1)
def main():
    monitor=CpuMonitor(server_id,db_config)
    monitor.run_once()
if __name__=="__main__":
    main()
