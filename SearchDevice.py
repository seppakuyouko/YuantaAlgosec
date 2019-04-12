import json
import requests
import urllib3
import sys
import datetime
import os
#import demjson
import operator
import xmltodict

def getSeesion():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = "https://10.255.63.32/AFA/php/ws.php"
    querystring = {"wsdl":""}

    payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:afa=\"https://www.algosec.com/afa-ws\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n      <afa:ConnectRequest>\r\n         <UserName>root</UserName>\r\n         <Password>1qazXSW@</Password>\r\n      </afa:ConnectRequest>\r\n   </soapenv:Body>\r\n</soapenv:Envelope>"
    headers = {
        'Content-Type': "application/xml",
        'cache-control': "no-cache",
        'Postman-Token': "b5081fbb-cda1-4d38-8e4e-2fb27a437fab"
        }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring,verify=False)
    tmpID=xmltodict.parse(response.text)
    return tmpID["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["ns1:ConnectResponse"]["SessionID"]

def getDeviceName(sess_ID):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = "https://10.255.63.32/AFA/php/ws.php"

    querystring = {"wsdl":""}

    payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:afa=\"https://www.algosec.com/afa-ws\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n      <afa:GetDevicesListRequest>\r\n         <SessionID>"+sess_ID+"</SessionID>\r\n      </afa:GetDevicesListRequest>\r\n   </soapenv:Body>\r\n</soapenv:Envelope>"
    headers = {
        'Content-Type': "application/xml",
        'cache-control': "no-cache",
        'Postman-Token': "cd886043-6e6f-4828-be6b-dd6e918512f6"
        }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring,verify=False)
    tmp=xmltodict.parse(response.text)
    devicetmpBox=[]
    for i in range(len(tmp["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["ns1:GetDevicesListResponse"]["Device"])):
        devicetmpBox.append(tmp["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["ns1:GetDevicesListResponse"]["Device"][i]["ID"])
        #print(tmp["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["ns1:GetDevicesListResponse"]["Device"][i]["ID"])
    # print(tmp["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["ns1:GetDevicesListResponse"]["Device"][0]["ID"])
    return devicetmpBox

if __name__=="__main__":
    deviceBox=[]
    sess_ID=getSeesion()
    deviceBox=getDeviceName(sess_ID)
    print(deviceBox)




