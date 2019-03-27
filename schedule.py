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
import xmltodict


if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = "https://10.255.63.32/AFA/php/ws.php"
    querystring = {"wsdl":""}
    payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:afa=\"https://www.algosec.com/afa-ws\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n      <afa:GetRulesByDeviceRequest>\r\n         <SessionID>b375b61ddfc96db556e6c46c08660cba</SessionID>\r\n         <DeviceID>192_168_95_239</DeviceID>\r\n      </afa:GetRulesByDeviceRequest>\r\n   </soapenv:Body>\r\n</soapenv:Envelope>"
    headers = {
        'Content-Type': "application/xml",
        'cache-control': "no-cache",
        'Postman-Token': "6f3995ee-1fe5-4470-87c4-842d91c1d131"
        }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring,verify=False)
    dict_string=xmltodict.parse(response.text)

    for i in range(len(dict_string['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:GetRulesByDeviceResponse']['Rules']['Rule'])):
        if(operator.eq(RuleID,dict_string['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:GetRulesByDeviceResponse']['Rules']['Rule'][i]['RuleID'])):
            return (dict_string['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:GetRulesByDeviceResponse']['Rules']['Rule'][i]['Schedule'])
            #print(dict_string['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:GetRulesByDeviceResponse']['Rules']['Rule'][i]['Schedule'])
            #print(dict_string['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:GetRulesByDeviceResponse']['Rules']['Rule'][i]['RuleID'])
