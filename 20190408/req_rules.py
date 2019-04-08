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
import xmltodict
import operator

app = Flask(__name__)
CORS(app)

@app.route('/compare', methods=['POST'])
def compare():
    sendJson=[]
    deviceName=request.form.get('deviceName')
    ddlCommentType=request.form.get('ddlCommentType')
    tb_OldComment=request.form.get('tb_OldComment')
    tb_NewComment=request.form.get('tb_NewComment')
    tb_Date_Start=request.form.get('tb_Date_Start')
    tb_Date_End=request.form.get('tb_Date_End')
    now_origintxt=""
    dateBox=[]


    if(operator.eq(ddlCommentType,"AddAndRemove")):
        #same time
        if(operator.eq(tb_Date_Start,tb_Date_End)):
            #pathStr
            origin_path="/var/www/html/ruleChange/"
            tb_Date_Starttmp=tb_Date_Start.split('-')
            dateStart=datetime.datetime(int(tb_Date_Starttmp[0]),int(tb_Date_Starttmp[1]),int(tb_Date_Starttmp[2]))

            yesterday = dateStart-datetime.timedelta(days=1)
            yesterday = yesterday.strftime("%Y-%m-%d")
            dateStart=dateStart.strftime("%Y-%m-%d")

            dateBox.append(dateStart)
            dateBox.append(yesterday)
            #today and yesterday

            for i in range(len(dateBox)):
                date_str=dateBox[i].split('-')
                tmp_path=origin_path+date_str[0]+"/"+date_str[1]
                #check the file exists or not
                if((os.path.isdir(tmp_path))and(os.path.exists(tmp_path+"/"+dateBox[i]+".txt"))):
                    file1 = open(tmp_path+"/"+dateBox[i]+".txt","r")
                    #print(tmp_path+"/"+dateBox[i]+".txt")
                    deviceBox=[]

                    for j in file1:
                        deviceBox.append(j)
                    #print(deviceBox)
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
                        #if user seleceted device Name
                        elif(operator.eq(jsonText['Rule'][k]['DeviceID'],deviceName)):
                            tmpJson=jsonText
                            #print(len(tmpJson['Rule']))
                            for l in range(len(tmpJson['Rule'])):
                                #select comments
                                if(operator.eq(tmpJson['Rule'][l]['Comment'],tb_OldComment)):
                                    tmpJson['Rule'][l]['c_date']=dateBox[i]
                                    sendJson.append(tmpJson['Rule'][l])
                                    break
            #print(sendJson)                        
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
                            tmpJson=jsonText
                            for l in range(len(tmpJson['Rule'])):
                                try:
                                    #select comments
                                    if(operator.eq(tmpJson['Rule'][l]['Comment'],tb_OldComment)):
                                        tmpJson['Rule'][l]['c_date']=dateBox[i]
                                        sendJson.append(tmpJson['Rule'][l])
                                except:
                                    pass
                        #if user seleceted device Name
                        elif(operator.eq(jsonText['Rule'][k]['DeviceID'],deviceName)):
                            tmpJson=jsonText
                            for l in range(len(tmpJson['Rule'])):
                                #select comments
                                if(operator.eq(tmpJson['Rule'][l]['Comment'],tb_OldComment)):
                                    tmpJson['Rule'][l]['c_date']=dateBox[i]
                                    sendJson.append(tmpJson['Rule'][l])
                                    break
    elif(operator.eq(ddlCommentType,"Edit")):
        origin_path="/var/www/html/ruleChange/"
        dateBox.append(tb_Date_Start)
        dateBox.append(tb_Date_End)
        for i in range(len(dateBox)):
                date_str=dateBox[i].split('-')
                tmp_path=origin_path+date_str[0]+"/"+date_str[1]
                #check the file exists or not
                if((os.path.isdir(tmp_path))and(os.path.exists(tmp_path+"/"+dateBox[i]+".txt"))):
                    #print(tmp_path+"/"+dateBox[i]+".txt")
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
                        #if user seleceted device Name
                        elif(operator.eq(jsonText['Rule'][k]['DeviceID'],deviceName)):
                            tmpJson=jsonText
                            for l in range(len(tmpJson['Rule'])):
                                #select comments
                                if(operator.eq(tmpJson['Rule'][l]['Comment'],tb_OldComment)):
                                    tmpJson['Rule'][l]['c_date']=dateBox[i]
                                    sendJson.append(tmpJson['Rule'][l])
                                    break
                    print(sendJson)

        # print(tb_OldComment)
        # print(tb_NewComment)
        # print(dateBox)



   
    finalSend=dealSendJson(sendJson,dateBox)
    return json.dumps(finalSend)
def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

def dealSendJson(sendJson,dateBox):
    chkDateBox=[]
    if(len(sendJson)>0):
        for i in range(len(dateBox)):
            chkDateBox.append(False)
        for i in range(len(sendJson)):
            for j in range(len(dateBox)):
                if(operator.eq(sendJson[i]['c_date'],dateBox[j])):
                    chkDateBox[j]=True
        # print(chkDateBox)
        for i in range(len(chkDateBox)):
            if(operator.eq(chkDateBox[i],False)):
                #print(dateBox[i])
                dict2=sendJson[0].copy() 
                for key,val in dict2.items():
                    if(operator.eq(key,"RuleID")):
                        dict2.update({key:sendJson[0]["RuleID"]})
                    elif(operator.eq(key,"c_date")):
                        dict2.update({key:dateBox[i]})
                    elif(operator.eq(key,"Comment")):
                        dict2.update({key:sendJson[0]["Comment"]})
                    else:
                        dict2.update({key:"N/A"})
                sendJson.append(dict2)
    
    
    return sendJson


@app.route('/dataFromAjax', methods=['POST'])
def dataFromAjax():
	sess_ID = request.form.get('sess_ID')
	device_name = request.form.get('device_name')
	
	
	datenow=datetime.datetime.now().strftime("%Y-%m-%d")
	datestr=datetime.datetime.now().strftime("%Y-%m-%d")
	datestr=datestr.split('-')
	year=datestr[0]
	month=datestr[1]
	
	# if not os.path.exists("/var/www/html/ruleChange/scripts/"+datestr):
		# print("folder")
		# os.makedirs("/var/www/html/ruleChange/scripts/"+datestr)
    
	f=open("/var/www/html/ruleChange/"+year+"/"+month+"/"+datenow+".txt","w")	
	session_text=sess_ID
	entity_box=device_name.split(',')
	for entity_text in entity_box:
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		url = "https://10.216.7.15/AFA/php/ws.php"
		querystring = {"wsdl":""}
		entity_text=entity_text.replace('.','_')
		payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:afa=\"https://www.algosec.com/afa-ws\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n      <afa:GetRulesByDeviceRequest>\r\n         <SessionID>"+str(session_text)+"</SessionID>\r\n         <DeviceID>"+entity_text+"</DeviceID>\r\n      </afa:GetRulesByDeviceRequest>\r\n   </soapenv:Body>\r\n</soapenv:Envelope>"
        	#print(payload)
		headers={
			'Content-Type': "application/xml",
			'cache-control': "no-cache",
		}
		response = requests.request("POST", url, data=payload, headers=headers, params=querystring,verify=False)
		# print(response.text)
		dict_string=xmltodict.parse(response.text)
		#print(dict_string)
		objectJson=json.dumps(dict_string['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:GetRulesByDeviceResponse']['Rules'], ensure_ascii=False)
		#print(objectJson)
		f.write(objectJson+"\n")
	f.close()
if __name__ == "__main__":
	app.run(ssl_context=('cert.pem','key.pem'))
    #app.run(host='10.216.7.15',ssl_context=('cert.pem','key.pem'))
	