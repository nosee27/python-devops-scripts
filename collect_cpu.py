#!/usr/bin/env python3
import psutil
import pymysql
import time
import sys
import os
db_config={
        'host':'localhost',
        'user':'root',
        'password':os.environ.get('MySQL_PASSWORD','password'),
        'database':'devops',
        'charset':'utf8mb4'
        }
server_id=1
def get_cpu_percent():
    return psutil.cpu_percent(interval=1)
def insert_cpu_percent(server_id,cpu_usage):
    connection=None
    cursor=None
    try:
        connection=pymysql.connect(**db_config)
        cursor=connection.cursor()

        sql="insert into cpu_history(server_id,timestamp,cpu_usage)values(%s,NOW(),%s)"

        cursor.execute(sql,(server_id,cpu_usage))
        connection.commit()
        print(f"{__name__},success:server_id={server_id},cpu_usage={cpu_usage}%")
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def main():
    cpu=get_cpu_percent()
    insert_cpu_percent(server_id,cpu)
if __name__=="__main__":
    main()
