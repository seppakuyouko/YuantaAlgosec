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




if __name__ == "__main__":
    datenow=datetime.datetime.now().strftime("%Y-%m-%d")
    datestr=datetime.datetime.now().strftime("%Y-%m-%d")
    datestr=datestr.split('-')
    year=datestr[0]
    month=datestr[1]
    path = 'D:\\'
    f=open("D:\\"+year+'\\'+month+"\\"+datenow+".txt","w")
    sessiontxt="b375b61ddfc96db556e6c46c08660cba"
    devicetxt="192_168_95_239,10_1_81_31,10_1_81_125_root"
    entity_box=devicetxt.split(',')
    for entity_text in entity_box:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url = "https://10.255.63.32/AFA/php/ws.php"
        querystring = {"wsdl":""}

        payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:afa=\"https://www.algosec.com/afa-ws\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n      <afa:GetRulesByDeviceRequest>\r\n         <SessionID>"+str(sessiontxt)+"</SessionID>\r\n         <DeviceID>"+entity_text+"</DeviceID>\r\n      </afa:GetRulesByDeviceRequest>\r\n   </soapenv:Body>\r\n</soapenv:Envelope>"
        headers = {
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