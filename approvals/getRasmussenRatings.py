from urllib2 import Request, urlopen, URLError
import re
from lxml import html
import requests
from bs4 import BeautifulSoup
import psycopg2

dbconnection = psycopg2.connect(database="orangetweets", user="postgres", password="pass", host="localhost", port="5432")
dbcursor = dbconnection.cursor()


requestedsite = "http://www.rasmussenreports.com/public_content/politics/trump_administration/trump_approval_index_history"
lastsnapshot = 20170124

request = Request(requestedsite)
response = urlopen(request)
groupslist =  response.read().split("\n")
enteredratings = 0
indexapprove = 0
timestamp = ""
listmonths = ["NA", "Jan", "Feb", "Mar", "Apr", "May"]
for i in groupslist:
	if re.search(r"<table", i) :
		enteredratings = 1
	if re.search(r"<\/table", i) :
		enteredratings = 0
		continue
	if enteredratings == 0 :
		continue
	else :
		try :
			m = re.search(r"([0-9]{2})-(.*?)-([0-9]{2})", i)
			month = "0" + str(listmonths.index(m.group(2)))
			timestamp = "20" + m.group(3) + month + m.group(1)
			indexapprove = 0
		except :
			pass
		if timestamp == "":
			continue
		if indexapprove < 4 :
			indexapprove = indexapprove + 1
			continue
		else :
			try :
				m = re.search(r"([0-9]{2})\%", i)
				rate = m.group(1)
				indexapprove = 0
				mykey = timestamp + "_rasmussen"
				print ("Insert into table", mykey)
				dbcursor.execute("INSERT INTO approvalratings (datesource, source, date,rating) VALUES (%s, %s, %s, %s);", (mykey, "rasmussen", timestamp, rate));
				dbconnection.commit()
			except :
				print ("Insert failed")
				pass

dbconnection.close()


			

