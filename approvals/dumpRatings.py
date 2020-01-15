
#import pandas_datareader.data as web
#import pandas_datareader as pdr
import pandas as pd
from datetime import datetime
import time
from datetime import date
from datetime import timedelta
import numpy as np
import re
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from plotly.offline import *
from plotly.graph_objs import *


today = date.today()
year = str(today.year)
month = today.month
day = today.day
localtime = time.asctime(time.localtime(time.time()))
localtime = re.sub(r" ", "_", localtime)
if (month < 10) :
   month = "0" + str(month)
else :
   month = str(month)
if (day < 10) :
   day = "0" + str(day)
else :
    day = str(day)

mydumpfile = "/tmp/ratings_" + year + month + day + "_" + localtime + ".txt"
f = open(mydumpfile, 'w')

conn = psycopg2.connect(database="orangetweets", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()

today = date.today()
sqlcommand = "SELECT * FROM approvalratings order by datesource"
cur.execute(sqlcommand)
results = cur.fetchall()
for i in results :
	print >> f, (i)

f.close()
conn.close()
