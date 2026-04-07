#!/usr/bin/env python3
import pymysql
import requests
from concurrent.futures import ThreadPoolExecutor,as_completed
db_config={
        'host':'localhost',
        'user':'root',
        'password':'Yang228056@',
        'database':'devops',
        'charset':'utf8mb4'
        }
connection=None
cursor=None
def query_server_ips():
    try:
        connection=pymysql.connect(**db_config)
        cursor=connection.cursor()
        cursor.execute("select ip from servers")
        rows = cursor.fetchall()
        ips = [row[0] for row in rows]
        return ips
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def call_api(ip):
    try:
        url="https://httpbin.org/ip"
        response=requests.get(url,timeout=5)
        response.raise_for_status()
        data=response.json()
        origin=data.get("origin","default")
        return ip,True,f"匹配成功ip为{origin}"
    except Exception as e:
        return ip,False,f"匹配失败原因为{e}"
def main():
    ips=query_server_ips()
    if not ips:
         print("没有获取到 IP 列表，请检查数据库")
         return
    with ThreadPoolExecutor(max_workers=5) as executor:
        results=executor.map(call_api,ips)
    for ip, success ,msg in results:
        status="success" if success else "lose"
        print(f"{ip}-{status}-{msg}")
if __name__=="__main__":
    main()


