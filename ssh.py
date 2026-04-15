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
def get_ssh_hosts():
    connection=None
    cursor=None
    hosts=[]
    try:
        connection=pymysql.connect(**de_config)
        cursor=connection.cursor()
        sql="select ip,ssh_user,ssh_password from servers"
        cursor.execute(sql)
        for row in cursor.fetchall():
            ip,user,pwd =row
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
    try:
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko(AutoAddPolicy))
        ssh.connect(
                hostname=host,username=user,password=password)
        stdin,stdout,stderr=ssh.exe_command(cmd)
        out=stdout.read().decode("utf-8")
        err=stderr.read().decode("utf-8")
    except Exception as e:
        print(e)
    finally:
        if ssh:
            ssh.close()
def main():
    hosts=get_ssh_hosts()
    if not hosts:
        print("no hosts")
        sys.exit(1)
    with ThreadPoolExecutor(max_worksers=5) as executor:
        future_to_hosts = {
                executor.submit(ssh_exec,ip,user,pwd):(ip,user)
                for ip,user,pwd in hosts
                }
        for future in as_completed(future_to_hosts):
            ip,user=future_to_hosts[future]
            try:
                host,out.err,success=future.result()
                if success:
                    print(
