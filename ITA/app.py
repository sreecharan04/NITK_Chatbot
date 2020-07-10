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
from tabulate import tabulate
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
	if stri.get("action")=="restaurant.menu":
		parameters = stri.get("parameters")
		webbrowser.open("file:///C:/Users/user/Desktop/ITA%20project/web/standard.html",new=new)
	 	#speech = "OK RESPONSE ARRIVED"
		speech_resp="Did you check out the menu? Now please order"
		print("Response:")
		print(speech_resp)
		return {
			"speech" : speech_resp,
			"displayText": speech_resp ,
			"source": "NITK_Management"
		}
	
	if stri.get("action")=="order.item":
		parameters = stri.get("parameters")
		quantity = str(parameters.get("number"))
		hostel = str(parameters.get("hostel_block"))
		food = str(parameters.get("food-product"))
		name = str(parameters.get("name"))
		phone = int(parameters.get("phone"))
		print(name)
		print(phone)
		quantity = quantity.replace("[","")
		quantity = quantity.replace("]","")
		quantity = quantity.replace(",","")
		quantity = quantity.split(" ")
		for i in range(len(quantity)):
			quantity[i] = int(quantity[i])
		food=str(food)
		
		food = food.replace("u'","")
		food = food.replace("[","")
		food = food.replace("]","")
		food = food.replace(",","")
		#food = food.replace("'","")
		food = food.split("'")
		food = food[:-1]
		for i in range(len(food)):
			if i!=0 :
				food[i]=food[i][1:]		
		price=[]
		sql="SELECT Price from mainorder where Dish=%s"
		for i in food:
			c.execute(sql,(i,))
			data = c.fetchall()
			print(data)
			price.append(data[0][0])
		bill_amt=0
		for i in range(len(price)):
			bill_amt+=quantity[i]*price[i]
		print(bill_amt)
		#sql= """INSERT INTO orderitem (order_amount,Name,phone) values (%s,%s,%s)"""
		c.execute("""INSERT INTO orderitem (order_amount,Name,phone) values (%s,%s,%s)""",(bill_amt,name,phone))
		conn.commit()
		sql= "SELECT max(orderid) FROM orderitem WHERE Name=%s"
		c.execute(sql,(name,))
		id = c.fetchall()
		id=id[0][0]
		for i in range(len(food)):
			c.execute("""INSERT INTO items (orderid,item_name,quantity) values (%s,%s,%s)""",(id,food[i],quantity[i]))
			conn.commit()
			sql="select max(orderid) from orderitem";
			c.execute(sql)
			data=c.fetchall()
			print(data)
			data=int(data[0][0])
		speech="Thanks for ordering with us.Your bill amount is "+str(bill_amt)+". Remember your bill id for future reference:"+str(data)
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "NITK_Management"
		}
		
	if stri.get("action")=="order.check":
		print('hi')
		parameters = stri.get("parameters")
		orderid = parameters.get("orderid")
		print(orderid)
		sql="SELECT item_name,quantity from items where orderid=%s"
		
		c.execute(sql,(orderid,))
		data = c.fetchall()
		speech=data
		if speech == []:
			speech="Sorry !! Your order id does not exist"
		else:
			for i in range(len(speech)):
				speech[i] = list(speech[i])

			#speech = "OK RESPONSE ARRIVED"
			print("Response:")
			speech = tabulate(speech,headers=['Item','Quantity'])
			print(speech)
			
			sql="select distinct order_amount from orderitem inner join items on orderitem.orderid=items.orderid where orderitem.orderid=%s"
			c.execute(sql,(orderid,))
			data=c.fetchall()
			speech=speech+"       "+"Bill amount : "+str(data[0][0])
		return {
			"speech" : speech,
			"displayText": speech ,
			"source": "NITK_Management"
		}
	
		
	if stri.get("action")=="library.book.search":
		parameters = stri.get("parameters")
		bookname = parameters.get("bookname")
	
		sql="SELECT Availability from library where bookname=%s"
		
		c.execute(sql,(bookname,))
		data = str(c.fetchall())
		avail_flag=int(data[2])
		if avail_flag == 0:
			speech = "Sorry the book is not available in the library.Please try again later."
		else:
			sql="SELECT bookname,Author,floor_no,shelf_no from library where bookname=%s"
			c.execute(sql,(bookname,))
			data = c.fetchall()
			speech=data
			
			for i in range(len(speech)):
				speech[i] = list(speech[i])
			#speech = "OK RESPONSE ARRIVED"
			print("Response:")
			speech = tabulate(speech,headers=['Book Name','Author','Floor no.','Shelf no.'])
			print(speech)
		return {
			"speech" : speech,
			"displayText": speech ,
			"source": "NITK_Management"
		}
		
	if stri.get("action")=="library.author.search":
		parameters = stri.get("parameters")
		authorname = parameters.get("Author")
	
		sql="SELECT Availability from library where Author=%s"
		
		c.execute(sql,(authorname,))
		data = str(c.fetchall())
		print(data)
		avail_flag=int(data[2])
		if avail_flag == 0:
			speech = "Sorry the book related to the author is not available currently in the library.Please try again later."
		else:
			sql="SELECT Author,bookname,floor_no,shelf_no from library where Author=%s"
			c.execute(sql,(authorname,))
			data = c.fetchall()
			speech=data
			
			for i in range(len(speech)):
				speech[i] = list(speech[i])
			#speech = "OK RESPONSE ARRIVED"
			print("Response:")
			speech = tabulate(speech,headers=['Author','Book Name','Floor no.','Shelf no.'])
			print(speech)
		return {
			"speech" : speech,
			"displayText": speech ,
			"source": "NITK_Management"
		}
	
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
		sql= "SELECT Warden,Contact_no FROM warden WHERE Block=%s"
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
		
		
	# module-3 faculty-search by depts.
    	
	if stri.get("action")=="faculty.search":
		parameters = stri.get("parameters")
		dept = str(parameters.get("faculty_dept")) 
		post = str(parameters.get("faculty_post"))
		if post == "Faculty":
			sql="SELECT * FROM faculty WHERE Department=%s"
			c.execute(sql,(dept,))
			print('\n')
		else:
			#print(dept,type(dept))
			sql= "SELECT * FROM faculty WHERE Department=%s and post=%s"
			c.execute(sql,(dept,post))
			print('\n')
		data = c.fetchall()
		print(data)
		speech=data
		for i in range(len(speech)):
			speech[i] = list(speech[i])
		#speech = "OK RESPONSE ARRIVED"
		print("Response:")
		speech = tabulate(speech,headers=['Name','Department','Qualification','Post'])
		print(speech)
		#print(speech)
		return {
			"speech" : speech,
			"displayText": speech ,
			"source": "NITK_Management"
		}
		
	
		
	# module-3 timing search.
    	
	if stri.get("action")=="timings.search":
		print('in action')
		parameters = stri.get("parameters")
		building = str(parameters.get("building")) 
		#print(dept,type(dept))
		sql= "SELECT open_timing,close_timing FROM timings WHERE Building=%s"
		c.execute(sql,(building,))
		print('\n')
		data = c.fetchall()
		speech=data
		
		for i in range(len(speech)):
			speech[i] = list(speech[i])
		#speech = "OK RESPONSE ARRIVED"
		print("Response:")
		print(speech)
		speech1="opening time : "+str(speech[0][0])
		speech2="closing time : "+str(speech[0][1])
		speech=speech1+"\n \n"+speech2
		#speech = tabulate(speech,headers=['Opening Time','Closing Time'])
		
		print(speech)
		return {
			"speech" : speech,
			"displayText": speech ,
			"source": "NITK_Management"
		}
		
	if stri.get("action")=="gpa.calculator":
		parameters = stri.get("parameters")
		pointer = str(parameters.get("pointer"))
		credits = str(parameters.get("credits"))
		no_courses = str(parameters.get("no_courses"))
		no_courses = int(no_courses)

		pointer = pointer.replace("[","")
		pointer = pointer.replace("]","")
		pointer = pointer.replace(",","")
		pointer = pointer.split(" ")
		for i in range(len(pointer)):
			pointer[i] = int(pointer[i])
			
		credits = credits.replace("[","")
		credits = credits.replace("]","")
		credits = credits.replace(",","")
		credits = credits.split(" ")
		for i in range(len(credits)):
			credits[i] = int(credits[i])
		print(pointer)
		print(credits)
		sum=0
		sgpa=0
		credit_sum=0
		for i in range(len(credits)):
			credit_sum+=credits[i]
		for i in range(no_courses):
			sum+=credits[i]*pointer[i]
		sum=float(sum)
		sgpa = sum/credit_sum
		sgpa = round(sgpa,2)
		speech="Your pointer is "+str(sgpa)
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "NITK_Management"
		}
		
	

			
	else:
		return {
			"speech" : "Try again",
			"displayText": "Try again",
			"source": "NITK_Management"
		}
		

conn.commit()
if __name__ == '__main__':
    port=int(os.getenv('PORT',5000))
    app.run(debug=True)#,ssl_context='adhoc')
