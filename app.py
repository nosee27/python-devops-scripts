#!/usr/bin/env python3
from flask import Flask,render_template,jsonify,request
import pymysql
import configparser
import os
app=Flask(__name__)

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
def handle_get():
    if request.method=='GET':
        connection=None
        cursor=None
        servers=[]
        try:
            connection=pymysql.connect(**db_config)
            cursor=connection.cursor()
            sql="select id,hostname,ip,cpu,mem from servers"
            cursor.execute(sql)
            for row in cursor.fetchall():
                servers.append({'id':row[0],'hostname':row[1],'ip':row[2],'cpu':row[3],'mem':row[4]})
            return jsonify(servers)
        except Exception as e:
            return jsonify({'error':str(e)}),500
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    if request.method=='POST':
        data=request.get_json()
        if not data:
            return jsonify({'error':'请求体必须是 JSON 格式'}),400
        required_fileds=['hostname','ip','cpu_cores','mem_gb']
        for field in required_fileds:
            if field not in data:
                return jsonify({'error':f'缺少必要字段: {field}'}),400
        hostname=data['hostname']
        ip=data['ip']
        cpu=data['cpu_cores']
        mem=data['mem_gb']

        connection=None
        cursor=None
        try:
            connection=pymysql.connect(**db_config)
            cursor=connection.cursor()
            sql='insert into servers (hostname,ip,cpu,mem)values(%s,%s,%s,%s)'
            cursor.execute(sql,(hostname,ip,cpu,mem))
            connection.commit()
            new_id=cursor.lastrowid
            return jsonify({
                'message':"success",
                'id':new_id,
                'hostname':hostname,
                'ip':ip,
                'cpu':cpu,
                'mem':mem
                }),201
        except Exception as e:
            return jsonify({'error': f'数据库错误: {str(e)}'}), 500
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()









if __name__=="__main__":
    app.run(
        port=5000,host='0.0.0.0',debug=True
        )
