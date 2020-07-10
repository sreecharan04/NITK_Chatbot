import datetime

# variables given time, did, date, purpose

mysql3  =  "select * from doctor where hid = hid and did = did" 
# execute and fetch the data

if (Check wheter the data is returned):
	mysql = "select * from table patient where pid = pid"
	# You have to execute the data.
	if(mysql returns data):
	    DateTime = date + time #cncat the string
		mysql1 = "select pid from appontment where did = did and adatetime = DateTime and hid = hid"
		# Execute the command and fetch the data
		if(mysql1 return data):
			if (mysql1.pid == pid):
				speech= "your appintment is already booked."
			else:
				speech = "There is another appointment at this time please select another time"
		else:
			m = datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%A')
			mysql = "select Time from available where did = did and Weekday = m"
			time_variable =  #Read the time form the data you get.
			time1 = time_variable[0:9]
			time2 = time_variable[9:17]
			timeA = datetime.datetime.strptime(time1, "%H:%M:%S")
			timeB = datetime.datetime.strptime(time2, "%H:%M:%S")
			timeC = datetime.datetime.strptime(time, "%H:%M:%S")
			if timeC >timeA and timeC < timeB:
			   add the data into the appointment table.
			else:
			   speech = "DOctor is not available at that time"			 
	else:
	    speech="Please register first and then book an appointment"
else:
    speech = "The doctor is not working in that hospital"