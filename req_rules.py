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
    sendJson=[]
    #sessionID=request.form.get('sess_ID')
    #entity_text=request.form.get('entity_text')
    deviceName=request.form.get('deviceName')
    tb_Comment=request.form.get('tb_Comment')
    tb_Date_Start=request.form.get('tb_Date_Start')
    tb_Date_End=request.form.get('tb_Date_End')
    now_origintxt=""

    #print(deviceName)
    #print(tb_Comment)
    #print(tb_Date_Start)
    #print(tb_Date_End)


    datenow=datetime.datetime.now().strftime("%Y-%m-%d")
    if(operator.eq(datenow,tb_Date_Start) and operator.eq(datenow,tb_Date_End)):
        #pathStr
        origin_path="/var/www/html/ruleChange/"
        yesterday = datetime.datetime.today()-datetime.timedelta(days=1)
        yesterday = yesterday.strftime("%Y-%m-%d")
        #count between date_start and date_end
        dateBox=[]
        dateBox.append(yesterday)

        #yesterday
        for i in range(len(dateBox)):
            date_str=dateBox[i].split('-')
            tmp_path=origin_path+date_str[0]+"/"+date_str[1]
            #check the file exists or not
            if((os.path.isdir(tmp_path))and(os.path.exists(tmp_path+"/"+dateBox[i]+".txt"))):
                file1 = open(tmp_path+"/"+dateBox[i]+".txt","r")
                deviceBox=[]
                for j in file1:
                    deviceBox.append(j)
                for k in range(len(deviceBox)):
                    jsonText=json.loads(deviceBox[k])
                    #if user selected all
                    if(operator.eq(deviceName,'All')):
                        tmpJson=jsonText['0']['rules']
                        for l in range(len(tmpJson)):
                            try:
                                #select comments
                                if(operator.eq(tmpJson[l]['comments'][0],tb_Comment)):
                                    tmpJson[l]['name']=jsonText['0']['name']
                                    tmpJson[l]['c_date']=dateBox[i]
                                    sendJson.append(tmpJson[l])
                            except:
                                pass
                    #if user seleceted device Name
                    elif(operator.eq(jsonText['0']['name'],deviceName)):
                        tmpJson=jsonText['0']['rules']
                        for l in range(len(tmpJson)):
                            #select comments
                            if(operator.eq(tmpJson[l]['comments'][0],tb_Comment)):
                                tmpJson[l]['name']=jsonText['0']['name']
                                tmpJson[l]['c_date']=dateBox[i]
                                #print(tmpJson[j])
                                sendJson.append(tmpJson[l])
                                #print(sendJson)
                        break
                    else:
                        pass
        #today
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url = "https://10.216.7.15/fa/server/rules/read"
            session_text=sessionID
            entity_box=entity_text.split(',')
            for entity_text in entity_box:
                querystring = {"session":session_text,"entity":entity_text}
                payload = ""
                headers = {
                    'cache-control': "no-cache",
                    'Postman-Token': "55f92497-1aa9-4fc9-acf9-0650a3b6546a"
                }
                response = requests.request("GET", url, data=payload, headers=headers, params=querystring,verify=False)
                now_origintxt+=response.text+"&%^"
            
            now_origintxt=now_origintxt.split("&%^")
            for i in range(len(now_origintxt)):
                jsonText=json.loads(deviceBox[k])
                #if user selected all
                if(operator.eq(deviceName,'All')):
                    tmpJson=jsonText['0']['rules']
                    for l in range(len(tmpJson)):
                        try:
                            #select comments
                            if(operator.eq(tmpJson[l]['comments'][0],tb_Comment)):
                                tmpJson[l]['name']=jsonText['0']['name']
                                tmpJson[l]['c_date']=dateBox[i]
                                sendJson.append(tmpJson[l])
                        except:
                            pass
                #if user seleceted device Name
                elif(operator.eq(jsonText['0']['name'],deviceName)):
                    tmpJson=jsonText['0']['rules']
                    for l in range(len(tmpJson)):
                        #select comments
                        if(operator.eq(tmpJson[l]['comments'][0],tb_Comment)):
                            tmpJson[l]['name']=jsonText['0']['name']
                            tmpJson[l]['c_date']=dateBox[i]
                            #print(tmpJson[j])
                            sendJson.append(tmpJson[l])
                            #print(sendJson)
                    break
                else:
                    pass 
        except Exception as e:
            fileError=open("/var/www/html/ruleChange/scripts/"+"error"+datenow+".txt","w")
            fileError.write(''.join(e.args)+"\n")
    else:
        #count between date_start and date_end
        dateBox=dateRange(tb_Date_Start, tb_Date_End)
        #pathStr
        origin_path="/var/www/html/ruleChange/"

        for i in range(len(dateBox)):
            date_str=dateBox[i].split('-')
            tmp_path=origin_path+date_str[0]+"/"+date_str[1]

            #check the file exists or not
            if((os.path.isdir(tmp_path))and(os.path.exists(tmp_path+"/"+dateBox[i]+".txt"))):
                file1 = open(tmp_path+"/"+dateBox[i]+".txt","r")
                deviceBox=[]
                for j in file1:
                    deviceBox.append(j)
                for k in range(len(deviceBox)):
                    jsonText=json.loads(deviceBox[k])
                    #if user selected all
                    if(operator.eq(deviceName,'All')):
                        tmpJson=jsonText['0']['rules']
                        for l in range(len(tmpJson)):
                            try:
                                #select comments
                                if(operator.eq(tmpJson[l]['comments'][0],tb_Comment)):
                                    tmpJson[l]['name']=jsonText['0']['name']
                                    tmpJson[l]['c_date']=dateBox[i]
                                    sendJson.append(tmpJson[l])
                            except:
                                pass
                    #if user seleceted device Name
                    elif(operator.eq(jsonText['0']['name'],deviceName)):
                        tmpJson=jsonText['0']['rules']
                        for l in range(len(tmpJson)):
                            #select comments
                            if(operator.eq(tmpJson[l]['comments'][0],tb_Comment)):
                                tmpJson[l]['name']=jsonText['0']['name']
                                tmpJson[l]['c_date']=dateBox[i]
                                #print(tmpJson[j])
                                sendJson.append(tmpJson[l])
                                #print(sendJson)
                        break
                    else:
                        pass
        #checkDifferent
        # cur_num=0
        # base_date=sendJson[0]['c_date']
        # print(base_date)
        # while cur_num<len(sendJson)-1:
        #     next_num=cur_num+1
        #     if(operator.eq(base_date,sendJson[next_num]['c_date'])):
        #         continue
        #     while next_num<len(sendJson):
        #         if(operator.eq(sendJson[cur_num]['ruleId'],sendJson[next_num]['ruleId'])):
        #             if not(operator.eq(sendJson[cur_num]['fromZone'],sendJson[next_num]['fromZone'])):
        #                 sendJson[next_num]['fromZone']+="(Diff)"
        #             try:
        #                 for i in range(len(sendJson[cur_num]['source'])):
        #                     if not(operator.eq(sendJson[cur_num]['source'][i],sendJson[next_num]['source'][i])):
        #                         sendJson[next_num]['source'][i]+="(Diff)"
        #             except:
        #                     sendJson[next_num]['source'][i-1]+="(Diff)"
                            
                            
        #             if not(operator.eq(sendJson[cur_num]['fromZone'],sendJson[next_num]['fromZone'])):
        #             if not(operator.eq(sendJson[cur_num]['fromZone'],sendJson[next_num]['fromZone'])):
        #             if not(operator.eq(sendJson[cur_num]['fromZone'],sendJson[next_num]['fromZone'])):
        #             if not(operator.eq(sendJson[cur_num]['fromZone'],sendJson[next_num]['fromZone'])):
        #             if not(operator.eq(sendJson[cur_num]['fromZone'],sendJson[next_num]['fromZone'])):
        #             if not(operator.eq(sendJson[cur_num]['fromZone'],sendJson[next_num]['fromZone'])):
        #         next_num+=1
        #     cur_num+=1
        #print(sendJson[0]['ruleNum'])


   
    
    
    # #count between date_start and date_end
    # dateBox=dateRange(tb_Date_Start, tb_Date_End)

    # #pathStr
    # origin_path="/var/www/html/ruleChange/"

    # for i in range(len(dateBox)):
    #     date_str=dateBox[i].split('-')
    #     tmp_path=origin_path+date_str[0]+"/"+date_str[1]

    #     #check the file exists or not
    #     if((os.path.isdir(tmp_path))and(os.path.exists(tmp_path+"/"+dateBox[i]+".txt"))):
    #         file1 = open(tmp_path+"/"+dateBox[i]+".txt","r")
    #         deviceBox=[]
    #         for j in file1:
    #             deviceBox.append(j)

    #         for k in range(len(deviceBox)):

    #             jsonText=json.loads(deviceBox[k])
    #             #if user selected all
    #             if(operator.eq(deviceName,'All')):
    #                 tmpJson=jsonText['0']['rules']
    #                 for l in range(len(tmpJson)):
    #                     try:
    #                         #select comments
    #                         if(operator.eq(tmpJson[l]['comments'][0],tb_Comment)):
    #                             tmpJson[l]['name']=jsonText['0']['name']
    #                             tmpJson[l]['c_date']=dateBox[i]
    #                             sendJson.append(tmpJson[l])
    #                     except:
    #                         pass
    #             #if user seleceted device Name
    #             elif(operator.eq(jsonText['0']['name'],deviceName)):
    #                 tmpJson=jsonText['0']['rules']
    #                 for l in range(len(tmpJson)):
    #                     #select comments
    #                     if(operator.eq(tmpJson[l]['comments'][0],tb_Comment)):
    #                         tmpJson[l]['name']=jsonText['0']['name']
    #                         tmpJson[l]['c_date']=dateBox[i]
    #                         #print(tmpJson[j])
    #                         sendJson.append(tmpJson[l])
    #                         #print(sendJson)
    #                 break
    #             else:
    #                 pass

  
  
    
    #print(file1.readline())
    #jsonstr=json.loads()
    # d = {'name': sessionID,'age': deviceName}
    # print(sessionID)
    # print(deviceName)
    
    return json.dumps(sendJson)
def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

if __name__ == '__main__':
    app.run()


 
# if __name__ == '__main__':
#     for date in dateRange('2016-10-01', '2017-01-01'):
#         print date

