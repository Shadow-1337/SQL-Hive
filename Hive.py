#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import urlparse
import socket
import time
import traceback
import select
import struct
import sys
import re
import os
import atexit
import MySQLdb
import ast
import string
import shutil
import datetime
import threading






PORT_NUMBER = 8000


SaveList = []



class threadOne(threading.Thread): 
	def run(self):
		connection = MySQLdb.connect(host=SQLip, port=SQLport, user=SQLuser, db=SQLdb, passwd=SQLpassword)
		c = connection.cursor()
		i = 0
		while True:
			if len(SaveList) > 0:
				i = i + 1
				
				if i == 50:
					i = 0
					connection.commit()
					c.close()
					connection.close()
					
					connection = MySQLdb.connect(host=SQLip, port=SQLport, user=SQLuser, db=SQLdb, passwd=SQLpassword)
					c = connection.cursor()
				
				FILE = SaveList[0][0]
				UID = SaveList[0][1]
				#print SaveList[0]
				#print FILE
				print UID
				
				try:
					pos = FILE[0].find('"alive":')
					ALIVE = (FILE[0])[pos+8:pos+9]
					
					pos = FILE[0].find('"model":"')
					pos2 = (FILE[0])[pos+9:].find('"')
					MODEL = (FILE[0])[pos+9:pos2-(pos-11)]
					
					pos = FILE[0].find('"items":')
					pos2 = FILE[0].find(',"state":{"vars":{"exposure":')
					ITEMS = (FILE[0])[pos+8:pos2]
					
					pos = FILE[0].find(',"state":{"vars":{"exposure":')
					STATE = (FILE[0])[pos+9:-1]
					
					pos = FILE[0].find('"pos":')
					pos2 = (FILE[0]).find('],')
					POS = ((FILE[0])[pos+7:pos2]).split(',')
					X = POS[0]
					Z = POS[1]
					Y = POS[2]	
					
					pos = FILE[0].find('"dir":')
					pos2 = (FILE[0])[pos+9:].find('],')
					DIR = ((FILE[0])[pos+7:pos2+(pos+9)]).split(',')
					DIR_X = DIR[0]
					DIR_Y = DIR[1]
					DIR_Z = DIR[2]
					
					pos = FILE[0].find('"up":')
					pos2 = (FILE[0])[pos+8:].find('],')
					UP = ((FILE[0])[pos+6:pos2+(pos+8)]).split(',')
					UP0 = UP[0]
					UP1 = UP[1]
					UP2 = UP[2]
					
					timestamp = str(datetime.datetime.today())
					#print DIR
					#time.sleep(20)
					
					sql = "INSERT INTO player (uid, model, queue, alive, items, state, x, y, z, dir_x, dir_y, dir_z, up_0, up_1, up_2) VALUES ('"+UID+"','"+MODEL+"','"+timestamp+"','"+ALIVE+"','"+ITEMS+"','"+STATE+"','"+X+"','"+Y+"','"+Z+"','"+DIR_X+"','"+DIR_Y+"','"+DIR_Z+"','"+UP0+"','"+UP1+"','"+UP2+"')"
					c.execute(sql)
					print "Added: " + UID
					list.remove(SaveList[0])
				except:
					print "Error: " + UID
					list.remove(SaveList[0])
			
	



#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		print self.path
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write("Hello World !")
		return
				
	def do_POST(self):
		
		length = int(self.headers.getheader('content-length'))
		data =  self.rfile.read(length)
		if data == "":
			data = "{}"
			
		Uid = "444444444444444"	
			
		if self.path == "/save":
			SaveList.append([data, Uid])
			
		self.send_response(200)
		self.end_headers()
		self.wfile.write(data)
		return	
		

		
	
	
try:
	
	threadOne().start()
	
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()