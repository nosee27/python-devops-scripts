#!/usr/bin/env python3
import pymysql
def main():
    config={
            "host":"localhost",
            "user":"root",
            "password":"Yang228056@",
            "database":"devops",
            "charset":"utf8mb4"
            }
    connection=None
    cursor=None

    try:
        connection=pymysql.connect(**config)
        print("lianjiechenggong")

        cursor=connection.cursor()
        sql="select * from servers;"
        cursor.execute(sql)

        results=cursor.fetchall()
        print("servers data are ")
        for row in results:
            print(row)
    except Exception as e:
        print(f"wrong{e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
if __name__=="__main__":
    main()
