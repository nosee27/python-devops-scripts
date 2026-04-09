#!/usr/bin/env python3
import paramiko
import sys
import pymysql
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
def get_ssh_hosts_from_db():
    hosts=[]
    try:
        connection=pymysql.connect(**db_config)
        cursor=connection.cursor()
        sql="select ip,ssh_user,ssh_password from servers"
        cursor.execute(sql)
        for row in cursor.fetchall():
            ip,user,pwd=row
            hosts.append((ip,user,pwd))
        return hosts
    except Exception as e:
        print(e)
        return[]
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def ssh_exec(host,user,password,cmd='df -h'):
    ssh=None
    try:
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host,username=user,password=password,timeout=5)
        stdin,stdout,stderr=ssh.exec_command(cmd)
        out=stdout.read().decode('utf-8')
        err=stderr.read().decode('utf-8')
        return host,out,err,True
    except Exception as e:
        return host,"",f"{e}",False
    finally:
        if ssh:
            ssh.close()
def main():
    hosts=get_ssh_hosts_from_db()
    if not hosts:
        print("没有找到可用的 SSH 主机信息，请检查数据库表 servers 中的 ssh_user/ssh_password 字段")
        sys.exit(1)
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_host={
                      executor.submit(ssh_exec,ip,user,pwd):(ip,user)
                for ip,user,pwd in hosts
                }
        for future in as_completed(future_to_host):
            ip,user=future_to_host[future]
            try:
                host,out,err,success=future.result()
                print(f"========== {host} (用户: {user}) ==========")
                if success:
                    print(out if out else "(无输出)")
                    if err:
                        print(f"[STDERR]\n{err}")
                else:
                    print(f"错误: {err}")
                print()
            except Exception as e:
                print(f"{ip} 执行异常: {e}\n")
if __name__=="__main__":
    main()







