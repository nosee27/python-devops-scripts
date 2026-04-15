#!/uer/bin/env python3
import pymysql
def main():
    config={
            "host":"localhost",
            "user":"root",
            "password":"Yang228056@",
            "database":"devops",
            "charset":"utf8mb4"
            }
    connection =None
    cursor=None
    try:
        connection=pymysql.connect(**config)
        cursor=connection.cursor()

        sql="select * from servers;"
        cursor.execute(sql)
        result=cursor.fetchall()
        for row in result:
            print(row)

    except Exception as e:
        print(e)
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()
if __name__=="__main__":
    main()
