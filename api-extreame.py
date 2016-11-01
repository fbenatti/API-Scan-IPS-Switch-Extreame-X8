#!/usr/bin/python

import re
import requests
from requests.auth import HTTPBasicAuth
import xmltodict, json
import sys


device = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]

def exec_command_xml(comando,device,user,passw):
	post_data = """
		<?xml version="1.0" encoding="UTF-8"?>
			<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
							   xmlns:xoscfg="urn:xapi/cfgmgmt/cfgmgr" 
							   xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" 
							   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
							   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
							   SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
				<SOAP-ENV:Body><xoscfg:execCli>
					<command>%s</command>
				</xoscfg:execCli>
			</SOAP-ENV:Body>
		</SOAP-ENV:Envelope>""" % comando
	
		
	j = requests.post('http://'+ device +'/xmlservice', data=post_data, auth=HTTPBasicAuth(user, passw), verify=False)
	o = xmltodict.parse(j.text)
	result =  o['SOAP-ENV:Envelope']['SOAP-ENV:Body']['xoscfg:execCliResponse']['reply']
	return result

def find_start_end_string(string,tp):
	#Trata inicio e fim da string
	a=0
	li = []
	if tp == 'vr':
		for i in string:
			if '-------------------------------------------------------------------------------' in i:
				li.append(a)
			a=a+1
		return [li[0]+1,li[1]]
	elif tp == 'vl':
		for i in string:
			if '-------------------------------------------------------------------------------' in i:
				li.append(a)
			a=a+1
		return [li[1]+1,li[2]]
		
	
def show_vr(device,user,passw):
	#Trata o resultado do comando show vr
	comando = "show vr"
	result_xml = exec_command_xml(comando,device,user,passw).split('\n')
	start_end_string = find_start_end_string(result_xml,'vr')
	for i in range (start_end_string[0],start_end_string[1]):
		print "IPs VR: %s" % result_xml[i].split()[0]
		show_iparp(result_xml[i].split()[0],device,user,passw)

					
def show_vlan(device,user,passw):
	#Trata o resultado do comando show vr
	comando = "show vlan"
	result_xml = exec_command_xml(comando,device,user,passw).split('\n')
	start_end_string = find_start_end_string(result_xml,'vl')
	for i in range (start_end_string[0],start_end_string[1]):
		bsip = result_xml[i]
		regex = re.findall(r"\d{1,3}(?:\.\d{1,3}){3}", bsip)
		if regex:
			if '1.1.1.1' not in regex:
				print regex
				
def show_iparp(comando,device,user,passw):
	comando = "show iparp vr %s" % comando
	result_xml = exec_command_xml(comando,device,user,passw)
	result_xml = result_xml.split()
	for i in result_xml:
		regex = re.findall(r"\d{1,3}(?:\.\d{1,3}){3}", i)
		if regex:
			print regex[0]
		
show_vr(device,user,password)








