import sqlite3
import csv

f=open('data.csv','r')

reader = csv.reader(f)

conn = sqlite3.connect('hospital1.db')

cur = conn.cursor()
			 
for row in reader:
	cur.execute("INSERT INTO AVAILABLE VALUES (?, ?, ?)", row)
	
f.close()
conn.commit()
conn.close()