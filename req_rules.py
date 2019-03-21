# -*- coding: utf-8 -*-
import requests
import urllib3
import sys
import datetime
import os
from flask import Flask, render_template, request
from flask import jsonify
import operator
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/compare', methods=['POST'])
def compare():
    deviceBox=[]
    sendJson=[]
    print(datetime.datetime.now().strftime("%Y/%m/%d"))
    # sessionID=request.form.get('sess_ID')
    deviceName=request.form.get('deviceName')
    tb_Comment=request.form.get('tb_Comment')
    tb_Date_Start=request.form.get('tb_Date_Start')
    tb_Date_End=request.form.get('tb_Date_End')
    
    # print(deviceName)
    # print(tb_Comment)
    # print(tb_Date_Start)
    # print(tb_Date_End)

    file1 = open("device.txt","r")
    for i in file1:
        deviceBox.append(i)

    for i in range(len(deviceBox)):
        jsonText=json.loads(deviceBox[i])
        if(operator.eq(deviceName,'All')):
            tmpJson=jsonText['0']['rules']
            for j in range(len(tmpJson)):
                try:
                     #select comments
                    if(operator.eq(tmpJson[j]['comments'][0],tb_Comment)):
                        tmpJson[j]['name']=jsonText['0']['name']
                        sendJson.append(tmpJson[j])
                except:
                    pass
        elif(operator.eq(jsonText['0']['name'],deviceName)):
            tmpJson=jsonText['0']['rules']
            for j in range(len(tmpJson)):
                #select comments
                if(operator.eq(tmpJson[j]['comments'][0],tb_Comment)):
                    tmpJson[j]['name']=jsonText['0']['name']
                    print(tmpJson[j])
                    sendJson.append(tmpJson[j])
            #print(sendJson)
            break
        else:
            pass

    

    #print(file1.readline())
    #jsonstr=json.loads()
    # d = {'name': sessionID,'age': deviceName}
    # print(sessionID)
    # print(deviceName)
    
    return json.dumps(sendJson)

if __name__ == '__main__':
    app.run()



