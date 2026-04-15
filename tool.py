#!/usr/bin/env python3
import os
import sys
import paramiko
import pymysql
import configparser
import argparse
from concurrent.fututrs import ThreadPoolExecutor,as_completed
config_file=os.path.expanduser("~/bin/config_ssh.ini")
def load_db_config():
    config=configparser.ConfigParser()
    config.read(config_file)
    return {
            'host':config.get('database','host'),
            'user':config.get('database','user'),
            'password':config.get('database','password'),
            'database':config.get('database','database'),
            'charset':config.get('database','charset')
            }
def get_ssh_config():
    db_config=load_db_config()
    hosts=[]
    try:
        connection=pymysql.connect(**db_config)
        cursor.connection.cursor()
        sql="select ip,ssh_user,ssh_password from servers"
        cursor.execute(sql)
        for row in cursor.fetchall():
            hosts.append((row[0],row[1],row[2]))
        connection.close()
        return hosts
    except Exception as e:
        print(e)
        return []
def ssh_exec(host,user,password,cmd,timeout):
    try:
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host,username=user,password=password,timeout=timeout)
        stdin,stdout,stderr=ssh.exec_command(cmd)
        out=stdout.read().decode("utf-8")
        err=stderr.read().decode("utf-8")
        ssh.close()
        return host,out,err,True
    except Exception as e:
        return host,"",str(e),False
def run_to_hosts(hosts,cmd,timeout,workers,quiet):
    if not hosts:
        print("kong")
        return
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures={
                executor.submit(ssh_exec,ip,user,pwd,cmd,timeout):(ip,user)
                for ip,user,pwd in hosts
                }
        for future in as_completed(futures):
            ip,user=futures[future]
            try:
                host,out,err,success=future.result()
                if not quiet:
                    print(f"========== {host} (用户: {user}) ==========")
                if success:
                    if out and not quiet:
                        print(out)
                    if err and not quiet:
                        print(f"{err}")
                else:
                    print(f"wrong is {err}")
                if not quiet:
                    print()
            except Exception as e:
                print(e)
def parse_args():
    p=argparse.ArgumentParser(description="并发 SSH 工具")
    p.add_argument("--hosts",nargs="+",help="")
    p.add_argument("--user",help="")
    p.add_argument("--password",help="")
    p.add_argument("--cmd",default="df -h",help="")
    p.add_argument("--timeout",type=int,default=5,help="")
    p.add_argument("--workers",type=int,default=5,help="")
    p.add_argument("--from-db",action="score_ture",help="")
    p.add_argument("--quiet",action="score_ture",help="")
    return p.parse_args()

def main():
    args=parse.args()
    if args.from_db:
        hosts=get_ssh_hosts
        if not hosts:
            print("no hosts")
            sys.exit(1)
        run_to_hosts(hosts,args.cmd,args.timeout,args.workers,args.quiet)
    elif args.hosts:
        if not args.user and not args.password:
            print("使用 --hosts 时必须同时提供 --user 和 --password")
            sys.exit(1)
        hosts=[(ip,user,password) for ip in hosts]
        run_to_hosts(hosts,args.cmd,args.timeout,arg.workers,args.quiet)
    else:
        print("no")
        sys.exit(1)

if __name__=="__main__":
    main()














