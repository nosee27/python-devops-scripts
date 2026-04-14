#!/usr/bin/env python3
from flask import Flask,render_template,jsonify,request
import pymysql
import configparser
import os
app=Flask(__name__)
def api_response(code,message,data=None):
    return jsonify({'code':code,'message':message,'data':data}),code
@app.route('/')
def hello():
    return render_template('index.html',message="welcome to devops!")
file_config=os.path.expanduser('~/bin/config.ini')
config=configparser.ConfigParser()
config.read(file_config)
db_config={
        'host':config.get('database','host'),
        'user':config.get('database','user'),
        'password':config.get('database','password'),
        'database':config.get('database','database'),
        'charset':config.get('database','charset')
}
@app.route('/api/servers',methods=['GET','POST'])
def insert_data():
    if request.method=='GET':
        connection=None
        cursor=None
        servers=[]
        try:
            connection=pymysql.connect(**db_config)
            cursor=connection.cursor()
            sql='select id,hostname,ip,cpu_cores,mem_gb from servers'
            cursor.execute(sql)
            for row in cursor.fetchall():
                servers.append({'id':row[0],'hostname':row[1],'ip':row[2],'cpu_cores':row[3],'mem_gb':row[4]})
            return api_response(200,"success",servers)
        except Exception as e:
            return api_response(400,f"no exit {str(e)}",None)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    if request.method=='POST':
        data=request.get_json()
        if not data:
            return api_response(404,"no exit data",None)
        fileds=['hostname','ip','cpu_cores','mem_gb']
        for filed in fileds:
            if filed not in data:
                return api_response(404,"no exit filed",None)
        hostname=data['hostname']
        ip=data['ip']
        cpu_cores=data['cpu_cores']
        mem_gb=data['mem_gb']

        connection=None
        cursor=None
        try:
            connection=pymysql.connect(**db_config)
            cursor=connection.cursor()
            sql='insert into servers (hostname,ip,cpu_cores,mem_gb)  values(%s,%s,%s,%s)'
            cursor.execute(sql,(hostname,ip,cpu_cores,mem_gb))
            connection.commit()
            new_id=cursor.lastrowid
            
            new_server={
                'id':new_id,
                'hostname':hostname,
                'ip':ip,
                'cpu_cores':cpu_cores,
                'mem_gb':mem_gb
                }
            return api_response(201,"success",new_server)
        except Exception as e:
            return api_response(400,f"wrong is {str(e)}",None)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

@app.route('/api/servers/<int:server_id>')
def get_server(server_id):
    connection = None
    cursor=None
    try:
        connection=pymysql.connect(**db_config)
        cursor=connection.cursor()
        sql='select id,hostname,ip,cpu_cores,mem_gb from servers where id = %s'
        cursor.execute(sql,(server_id))
        
        row=cursor.fetchone()
        if not row:
            return api_response(404,"no exit",None)
        server={
                'id':row[0],
                'hostname':row[1],
                'ip':row[2],
                'cpu_cores':row[3],
                'mem_gb':row[4]
                }
        return api_response(200,'success',server)
    except Exception as e:
        return api_response(500,f"wrong,{str(e)}",None)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__=="__main__":
    app.run(
        port=5000,host='0.0.0.0',debug=True
        )
