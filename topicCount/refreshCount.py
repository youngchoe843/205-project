# import libraries, initialize
#from pandas.io.data import DataReader

import pandas_datareader.data as web
import pandas_datareader as pdr
import pandas as pd
from datetime import datetime
from datetime import date
from datetime import timedelta
import numpy as np
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from plotly.offline import *
from plotly.graph_objs import *

# get the range of dates for which we want daily stock prices
#Connecting to tcount
conn = psycopg2.connect(database="orangetweets", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()
truncateSQL= "DELETE FROM topicCount"
cur.execute(truncateSQL)
conn.commit()

refreshSQL = '''INSERT INTO topicCount (tweet_date, topic_id, topic_count) 
select tweet_date, topic_id, count(*) 
from tweettable 
where topic_id IS NOT NULL
group by tweet_date, topic_id'''

cur.execute(refreshSQL)
conn.commit()
