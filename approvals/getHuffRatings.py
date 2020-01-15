from __future__ import absolute_import, print_function, unicode_literals
import time
from time import time,ctime,gmtime,strftime,sleep
import itertools
from streamparse.spout import Spout
from urllib2 import Request, urlopen, URLError
import re
import requests
import psycopg2
from datetime import *
import pollster

# delete from approvalratings where source='huffpost';
dbconnection = psycopg2.connect(database="orangetweets", user="postgres", password="pass", host="localhost", port="5432")
dbcursor = dbconnection.cursor()
api = pollster.Api()

charts = api.charts_get(cursor=None)

for i in range(charts.count) :
        if charts.items[i].slug == "trump-job-approval" :
                index_job_approval = i
                break

dbcursor.execute("DELETE FROM approvalratings WHERE source='huffpost';");
dbconnection.commit()
insertedary = dict()
chart_slug = charts.items[index_job_approval].slug
trendlines = api.charts_slug_pollster_trendlines_tsv_get(chart_slug)
for i in range(len(trendlines)) :
	if trendlines.values[i][0] == "Approve" :
		month = trendlines.values[i][1].month
		day = trendlines.values[i][1].day
		year = trendlines.values[i][1].year
		rate = int(trendlines.values[i][2] + 0.5)
		if month < 10 :
			month = "0" + str(month)
		if day < 10 :
			day = "0" + str(day)
		timestamp = str(year) + str(month) + str(day)
                mykey = timestamp + "_huffpost"
		if (len(insertedary) > 0) and (mykey in insertedary) :
			continue	
#		if (int(timestamp) < 20170413) :
#			continue
#		sleep(1)
		try :
			print ("Insert into table", mykey)
        		dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);", (mykey, "huffpost", timestamp, rate));
        		dbconnection.commit() 
		except :
			print ("Insert failed")
		insertedary.update({mykey:1})

dbconnection.close()
