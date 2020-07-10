#!/usr/bin/env python
# coding:utf-8

import urllib
import json
from flask import *
import json,requests,sys
import apiai
import sqlite3
import datetime
import os
import mysql.connector
import webbrowser
new=2

app = Flask(__name__)

CLIENT_ACCESS_TOKEN = '27f2781372f64d5191947020e6930446'

ai= apiai.ApiAI(CLIENT_ACCESS_TOKEN)

conn = mysql.connector.connect(user='root',password='newrootpassword',
							   host='127.0.0.1',database='ita'
							   )
c = conn.cursor()

@app.route('/')
def main():
	return render_template('main.html')
@app.route('/home')
def index():
    return render_template('console.html')


@app.route('/webhook',methods=["POST"])
def webhook():
	req = request.get_json(silent=True, force=True)
	#print "Request:"
	#print json.dumps(req, indent=4)
	res = makeWebhookResult(req)
	res = json.dumps(res, indent=4)
	#print res
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r


def makeWebhookResult(req):
	#if req.get("result").get("action")!="interest":
	#	return {}
	stri = req.get("result")
	
	## our work starts here-module 1	
	if stri.get("action")=="academic.calendar":
		parameters = stri.get("parameters")
		year = str(parameters.get("academic_calendar-year")) 
		semester= str(parameters.get("calendar_semester"))
		print("\n")
		print(year+'\n'+semester+'\n')
		sql= "SELECT calendar_link FROM calendar WHERE year = %s AND semester = %s "
		c.execute(sql,(year,semester))
		data = str(c.fetchall())
		speech = data[4:-4] ;
		webbrowser.open(speech,new=new)
	 	#speech = "OK RESPONSE ARRIVED"
		speech_resp="Did you check out the calendar? Is there anything else that i can do for you?"
		print("Response:")
		print(data)
		print(speech_resp)
		return {
			"speech" : speech_resp,
			"displayText": speech_resp ,
			"source": "NITK_Management"
		}
		
	# module-2 block_wardens
    	
	if stri.get("action")=="hostel.wardens":
		parameters = stri.get("parameters")
		block = str(parameters.get("hostel_block")) 
		print("\n")
		print(block,type(block))
		sql= "SELECT Warden_name,Warden_nb FROM block WHERE Block=%s "
		c.execute(sql,(block,))
		data = str(c.fetchall())
		speech = data[4:-4];
	 	#speech = "OK RESPONSE ARRIVED"
		print("Response:")
		print(speech)
		#print(speech)
		return {
			"speech" : speech,
			"displayText": speech ,
			"source": "NITK_Management"
		}
		
		
	else:
		return {
			"speech" : "Try again",
			"displayText": "Try again",
			"source": "NITK_Management"
		}


if __name__ == '__main__':
    port=int(os.getenv('PORT',5000))
    app.run(debug=True)#,ssl_context='adhoc')
	