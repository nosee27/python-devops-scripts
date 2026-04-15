#!/usr/bin/env python3
import sys
import pymysql
def main():
    if len(sys.argv)!=3:
        print("wrong")
        sys.exit(1)
    try:
        server_id=int(sys.argv[1])
        cpu_usage=float(sys.argv[2])
    except Exception as e:
        print({e})
        exit(1)

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
        cursor=connection.cursor()

        sql="insert into cpu_history(server_id,timestamp,cpu_usage)values(%s,NOW(),%s)"
        cursor.execute(sql,(server_id,cpu_usage))
        connection.commit()
        print("success")
    except Exception as e:
        print({e})
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()
if __name__=="__main__":
    main()
