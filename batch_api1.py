#!usr/bin/env python3
import pymysql
import requests
from concurrent.futures import ThreadPoolExecutor
db_config={
        'host':'localhost',
        'user':'root',
        'password':'Yang228056@',
        'database':'devops',
        'charset':'utf8mb4'
        }
connection=None
cursor=None
def get_ips_from_db():
    try:
        ips=[]
        connection=pymysql.connect(**config)
        cursor=connection.cursor()
        sql="select ip from servers"
        cursor.execute(sql)
        for row in cursor.fetchall():
            ips.append(row[0])
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
        origin=data.get('origin','')
        return ip,True,f"{origin}"
    except Exception as e:
        return ip,False,f"{e}"
def main():
    ips=get_ips_from_db()
    if not ips:
        print("no ips")
        return
    with ThreadPoolExecutor(max_workers=5) as executor:
        results=executor.map(call_api,ips)
    for ip,success,msg in results:
        status="成功" if success else "失败"
        print(f"{ip}-{status}-{msg}")

if __name__=="__main__":
    main()









