# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask import jsonify
from flask_cors import CORS
import json
import requests
import urllib3
import sys
import datetime
import os
#import demjson
import operator

app = Flask(__name__)
CORS(app)

@app.route('/compare', methods=['POST'])
def compare():
    sendJson=[]
    #getSchedule()

    #sessionID=request.form.get('sess_ID')
    #entity_text=request.form.get('entity_text')
    deviceName=request.form.get('deviceName')
    tb_OldComment=request.form.get('tb_OldComment')
    tb_Date_Start=request.form.get('tb_Date_Start')
    tb_Date_End=request.form.get('tb_Date_End')
    now_origintxt=""

    #print(deviceName)
    #print(tb_OldComment)
    #print(tb_Date_Start)
    #print(tb_Date_End)
   

    #same time
    if(operator.eq(tb_Date_Start,tb_Date_End)):
        #pathStr
        origin_path="/var/www/html/ruleChange/"
        tb_Date_Starttmp=tb_Date_Start.split('-')
        dateStart=datetime.datetime(int(tb_Date_Starttmp[0]),int(tb_Date_Starttmp[1]),int(tb_Date_Starttmp[2]))

        yesterday = dateStart-datetime.timedelta(days=1)
        yesterday = yesterday.strftime("%Y-%m-%d")
        dateStart=dateStart.strftime("%Y-%m-%d")

        dateBox=[]
        dateBox.append(dateStart)
        dateBox.append(yesterday)
        #print(dateBox)

        #today and yesterday

        for i in range(len(dateBox)):
            date_str=dateBox[i].split('-')
            tmp_path=origin_path+date_str[0]+"/"+date_str[1]
            # print(os.path.isdir(tmp_path))
            # print(os.path.exists(tmp_path+"/"+dateBox[i]+".txt"))

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
                        tmpJson=jsonText
                        for l in range(len(tmpJson['Rule'])):
                            try:
                                #select comments
                                if(operator.eq(tmpJson['Rule'][l]['Comment'],tb_OldComment)):
                                    tmpJson['Rule'][l]['c_date']=dateBox[i]
                                    sendJson.append(tmpJson['Rule'][l])
                            except:
                                pass
    #                 #if user seleceted device Name
    #                 elif(operator.eq(jsonText['0']['name'],deviceName)):
    #                     tmpJson=jsonText['0']['rules']
    #                     for l in range(len(tmpJson)):
    #                         #select comments
    #                         if(operator.eq(tmpJson[l]['comments'][0],tb_Comment)):
    #                             tmpJson[l]['name']=jsonText['0']['name']
    #                             schedulestr=getSchedule(tmpJson[l]['ruleId'])
    #                             #print(schedulestr)
    #                             tmpJson[l]['schedule']=schedulestr
    #                             tmpJson[l]['c_date']=dateBox[i]
    #                             sendJson.append(tmpJson[l])
    #                     break
    #                 else:
    #                     pass
    #             #print(sendJson)            
    # else:
    #     #count between date_start and date_end
    #     dateBox=dateRange(tb_Date_Start, tb_Date_End)
    #     #pathStr
    #     origin_path="/var/www/html/ruleChange/"

    #     for i in range(len(dateBox)):
    #         date_str=dateBox[i].split('-')
    #         tmp_path=origin_path+date_str[0]+"/"+date_str[1]

    #         #check the file exists or not
    #         if((os.path.isdir(tmp_path))and(os.path.exists(tmp_path+"/"+dateBox[i]+".txt"))):
    #             file1 = open(tmp_path+"/"+dateBox[i]+".txt","r")
    #             deviceBox=[]
    #             for j in file1:
    #                 deviceBox.append(j)
    #             for k in range(len(deviceBox)):
    #                 jsonText=json.loads(deviceBox[k])
    #                 #if user selected all
    #                 if(operator.eq(deviceName,'All')):
    #                     tmpJson=jsonText['0']['rules']
    #                     for l in range(len(tmpJson)):
    #                         try:
    #                             #select comments
    #                             if(operator.eq(tmpJson[l]['comments'][0],tb_Comment)):
    #                                 tmpJson[l]['name']=jsonText['0']['name']
    #                                 schedulestr=getSchedule(tmpJson[l]['ruleId'])
    #                                 #print(schedulestr)
    #                                 tmpJson[l]['schedule']=schedulestr                                 
    #                                 tmpJson[l]['c_date']=dateBox[i]
    #                                 sendJson.append(tmpJson[l])
    #                         except:
    #                             pass
    #                 #if user seleceted device Name
    #                 elif(operator.eq(jsonText['0']['name'],deviceName)):
    #                     tmpJson=jsonText['0']['rules']
    #                     for l in range(len(tmpJson)):
    #                         #select comments
    #                         if(operator.eq(tmpJson[l]['comments'][0],tb_Comment)):
    #                             tmpJson[l]['name']=jsonText['0']['name']
    #                             schedulestr=getSchedule(tmpJson[l]['ruleId'])
    #                             #print(schedulestr)
    #                             tmpJson[l]['schedule']=schedulestr
    #                             tmpJson[l]['c_date']=dateBox[i]
    #                             sendJson.append(tmpJson[l])
    #                             #print(sendJson)
    #                     break
    #                 else:
    #                     pass
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

@app.route('/dataFromAjax', methods=['POST'])
def dataFromAjax():
	sess_ID = request.form.get('sess_ID')
	device_name = request.form.get('device_name')
	print(sess_ID)
	print(device_name)
	d = {'sess_ID': sess_ID,'device_name':device_name}
	
	x=datetime.datetime.now().strftime("%Y-%m-%d")
	datestr=datetime.datetime.now().strftime("%Y-%m-%d")
	datestr=datestr.split('-')
	year=datestr[0]
	month=datestr[1]
	
	# if not os.path.exists("/var/www/html/ruleChange/scripts/"+datestr):
		# print("folder")
		# os.makedirs("/var/www/html/ruleChange/scripts/"+datestr)
	f=open("/var/www/html/ruleChange/"+year+"/"+month+"/"+x+".txt","w")
	
	#f=open("/var/www/html/ruleChange/scripts/"+x+".txt","w")
	
	try:
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		url = "https://10.216.7.15/fa/server/rules/read"
		session_text=sess_ID
		entity_box=device_name.split(',')
		responsestr=""
		for entity_text in entity_box:
			querystring = {"session":session_text,"entity":entity_text}
			payload = ""
			headers = {
				'cache-control': "no-cache",
				'Postman-Token': "55f92497-1aa9-4fc9-acf9-0650a3b6546a"
			}
			response = requests.request("GET", url, data=payload, headers=headers, params=querystring,verify=False)
			f.write(response.text+"&%^"+"\n")
			responsestr+=response.text
		d = {'responsestr':responsestr}
		return jsonify(d)
	except Exception as e:
		fileError=open("/var/www/html/ruleChange/scripts/"+"error"+x+".txt","w")
		fileError.write(''.join(e.args)+"\n")
		print(''.join(e.args)+"\n")
		fileError.close()
		return '123'
	
	f.close()


if __name__ == "__main__":
	app.run(ssl_context=('cert.pem','key.pem'))
    #app.run(host='10.216.7.15',ssl_context=('cert.pem','key.pem'))
	