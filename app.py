#!/usr/bin/env python3
from flask import Flask,render_template,jsonify
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
@app.route('/api/servers')
def get_servers():
    connection=None
    cursor=None
    servers=[]
    try:
        connection=pymysql.connect(**db_config)
        cursor=connection.cursor()
        sql="select id,hostname,ip,cpu,mem from servers"
        cursor.execute(sql)
        for row in cursor.fetchall():
            servers.append({"id":row[0],
                           "hostname":row[1],
                           "ip":row[2],
                           "cpu_cores":row[3],
                           "mem_go":row[4]})
        return jsonify(servers)
    except Exception as e:
        return jsonify({"error":str(e)}),500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
if __name__=="__main__":
    app.run(
        port=5000,host='0.0.0.0',debug=True
    )
