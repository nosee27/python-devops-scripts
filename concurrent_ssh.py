#!/usr/bin/env python3
import sys
import os
import pymysql
import paramiko
from concurrent.futures import ThreadPoolExecutor,as_completed
import configparser
config_file=os.path.expanduser("~/bin/config_ssh.ini")
config=configparser.ConfigParser()
config.read(config_file)
db_config={
        'host':config.get('database','host'),
        'user':config.get('database','user'),
        'password':config.get('database','password'),
        'database':config.get('database','database'),
        'charset':config.get('database','charset')}
ssh_command=config.get('ssh','command')
ssh_timeout=config.getint('ssh','timeout')
ssh_max_workers=config.getint('ssh','max_workers')
def get_ssh_hosts():
    connection=None
    cursor=None
    hosts=[]
    try:
        connection=pymysql.connect(**db_config)
        cursor=connection.cursor()
        sql="select ip,ssh_user,ssh_password from servers"
        cursor.execute(sql)
        for row in cursor.fetchall():
            ip,user,password = row
            hosts.append((ip,user,password))
        return hosts
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def ssh_exec(host,user,password,cmd=ssh_command,timeout=ssh_timeout):
    try:
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host,username=user,password=password,timeout=timeout)
        stdin,stdout,stderr=ssh.exec_command(cmd)
        out=stdout.read().decode("utf-8")
        err=stderr.read().decode("utf-8")
        return host,out,err,True
    except Exception as e:
        return host,"",str(e),False
    finally:
        if ssh:
            ssh.close()
def main():
    hosts=get_ssh_hosts()
    if not hosts:
        sys.exit(1)
    with ThreadPoolExecutor(max_workers=ssh_max_workers) as executor:
        future_to_hosts={
                executor.submit(ssh_exec,ip,user,pwd):(ip,user)
                for ip,user,pwd in hosts
                }
        for future in as_completed(future_to_hosts):
            ip,user=future_to_hosts[future]
            try:
                host,out,err,success=future.result()
                if success:
                    if out:
                        print(out)
                    if err:
                        print(err)
                else:
                    print(f"worng is {err}")
            except Exception as e:
                print(e)

if __name__=="__main__":
    main()








