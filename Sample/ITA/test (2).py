import sqlite3
import datetime
conn = sqlite3.connect('hospital1.db')
#result = req.get("result")
#parameters = result.get("parameters")
pid = "1"#str(parameters.get("pid"))
time = "10:00:00"#str(parameters.get("time"))
date = "2018-04-24"#str(parameters.get("date"))
did = "2"#str(parameters.get("did"))
purpose = "cold"#str(parameters.get("purpose"))
location = "panaji"#str(parameters.get("location"))

dictionary = {"mangalore" : 1, "panaji" : 2, "jaipur" : 3, "salem" : 4, "vijayawada" : 5}

if location in dictionary.keys():
	hid = str(dictionary[location.lower()])
	cursor = conn.execute("SELECT * FROM DOCTOR WHERE DID = " + did + " AND HID = " + hid)
	data = cursor.fetchall()
	
	if len(data) != 0:
		print "ok1"
		cursor = conn.execute("SELECT * FROM PATIENT WHERE PID = " + pid)
		data = cursor.fetchall()
		
		if len(data) != 0:
			DateTime = date + " " + time
			cursor = conn.execute("SELECT PID FROM APPOINTMENT WHERE DID = " + did + " AND ADATETIME = \"" + DateTime + "\" AND HID = " + hid)
			data = cursor.fetchall()
			
			if len(data) != 0:
				if pid in data:
					speech = "Your appointment is already booked for the given time and doctor."
				else:
					speech = "The requested doctor already has appointment in the given time. Please book for another time."
			
			else:
				m = datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%A')
				cursor = conn.execute("SELECT TIME FROM AVAILABLE WHERE WEEKDAY = \""+m+"\"")
				time_variable = cursor.fetchone()[0]
				time_variable= str(time_variable)				
				time1, time2 = time_variable.split("-")
				time1=str(time1)
				print time1
				timeA = datetime.datetime.strptime(time1, "%H:%M:%S")
				timeB = datetime.datetime.strptime(time2, "%H:%M:%S")
				timeC = datetime.datetime.strptime(time, "%H:%M:%S")
				if timeC >timeA and timeC < timeB:
					cursor = conn.execute("INSERT INTO APPOINTMENT(PID, DID, HID, PURPOSE, ADATETIME, AFEE) VALUES(" + pid + ", " + did + ", " + hid + ", \"" + purpose + "\", \"" + DateTime + "\", 0)")
					speech = "Your appointment is booked at "+ time +" on "+ date
				else:
					speech = "The requested doctor is unavailable at the requested time. Please book for another time."
		else:
			speech="The patient does not exist in the records. Please try again or register before booking an appointment."
	else:
		speech = "The doctor does not exist in the records and/or the doctor does not work in the given hospital. Please try again."
else:
	speech = "The location does not exist in the records. Please try again."


print speech