from __future__ import absolute_import, print_function, unicode_literals
from time import time,ctime,gmtime,strftime,sleep
import itertools
from streamparse.spout import Spout
from urllib2 import Request, urlopen, URLError
import re
import requests
import psycopg2
from datetime import *


dbconnection = psycopg2.connect(database="orangetweets", user="postgres", password="pass", host="localhost", port="5432")
dbcursor = dbconnection.cursor()

'''
try :
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170124_gallup", "gallup",20170124, 46));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170126_gallup", "gallup",20170126, 45));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170127_gallup", "gallup",20170127, 42));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170129_gallup", "gallup",20170129, 43));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170203_gallup", "gallup",20170203, 44));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170204_gallup", "gallup",20170204, 42));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170207_gallup", "gallup",20170207, 43));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170209_gallup", "gallup",20170209, 42));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170210_gallup", "gallup",20170210, 41));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170211_gallup", "gallup",20170211, 40));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170216_gallup", "gallup",20170216, 38));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170217_gallup", "gallup",20170217, 40));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170218_gallup", "gallup",20170218, 41));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170219_gallup", "gallup",20170219, 42));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170220_gallup", "gallup",20170220, 41));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170221_gallup", "gallup",20170221, 42));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170222_gallup", "gallup",20170222, 43));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170224_gallup", "gallup",20170224, 41));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170225_gallup", "gallup",20170225, 41));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170226_gallup", "gallup",20170226, 42));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170228_gallup", "gallup",20170228, 43));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170305_gallup", "gallup",20170305, 44));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170306_gallup", "gallup",20170306, 43));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170307_gallup", "gallup",20170307, 42));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170308_gallup", "gallup",20170308, 41));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170309_gallup", "gallup",20170309, 42));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170310_gallup", "gallup",20170310, 44));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170311_gallup", "gallup",20170311, 45));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170312_gallup", "gallup",20170312, 42));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170313_gallup", "gallup",20170313, 39));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170314_gallup", "gallup",20170314, 40));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170315_gallup", "gallup",20170315, 42));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170316_gallup", "gallup",20170316, 41));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170317_gallup", "gallup",20170317, 40));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170318_gallup", "gallup",20170318, 37));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170319_gallup", "gallup",20170319, 39));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170321_gallup", "gallup",20170321, 40));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170322_gallup", "gallup",20170322, 39));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170323_gallup", "gallup",20170323, 41));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170325_gallup", "gallup",20170325, 40));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170326_gallup", "gallup",20170326, 36));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170328_gallup", "gallup",20170328, 35));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170329_gallup", "gallup",20170329, 38));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170331_gallup", "gallup",20170331, 40));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170401_gallup", "gallup",20170401, 38));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170403_gallup", "gallup",20170403, 39));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170404_gallup", "gallup",20170404, 42));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170405_gallup", "gallup",20170405, 41));
	dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170406_gallup", "gallup",20170406, 40));
        dbcursor.execute("INSERT INTO approvalratings (datesource, source, date, rating) VALUES (%s, %s, %s, %s);",  ("20170411_gallup", "gallup",20170411, 41));
except:
	pass
'''


l = "http://www.gallup.com/home.aspx"
r = requests.get(l)
rate = re.search(r'(.*?gallup-daily-trump-job-approval.aspx\"\>).*?\n.*?([0-9]{2})\%.*?\n', r.text).group(2)
timestamp = str(date.today()).replace('-', '')
mykey = timestamp + "_gallup"
print ("Insert into table", mykey)
try :
        mykey = timestamp + "_gallup"
        dbcursor.execute("INSERT INTO approvalratings (datesource, source, date,rating) VALUES (%s, %s, %s, %s);", (mykey, "gallup", timestamp, rate));
        dbconnection.commit()
except :
        print ("Insert failed")

dbconnection.close()
