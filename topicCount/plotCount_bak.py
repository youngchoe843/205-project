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

numTopics = 5

# get the range of dates for which we want daily stock prices
#Connecting to tcount
conn = psycopg2.connect(database="orangetweets", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()

topTopicsSQL = "SELECT topic_id, count(topic_count) as ttl FROM topicCount ORDER BY ttl DESC LIMI" + str(numTopics)
print (topTopicsSQL)
ttlCount = pd.read_sql(topTopicsSQL, conn)
print(ttlCount[0])

for topicIdx in numTopics:
	plotSQL = "SELECT tweet_date, topic_id, topic_count FROM topicCount WHERE topic_id = " + str(ttlCount[0][topicIdx])
	print(plotSQL)

ttlCount = pd.read_sql(plotSQL, conn)



# plot the stock prices with annotations for important dates
trace1 = Scatter(
    x=ttlCount["tweet_date"],
    y=ttlCount["topic_count"],
	line=Line(
        color='rgb(0,116,217)'
    ),
    name=ttlCount["topic_id"][0],
)
trace2 = Scatter(
    x=allStocks["tickerdate"],
    y=allStocks["lmt"],
	line=Line(
        color='rgb(255,0,85)'
    ),
    name='Lockheed Martin'
)
trace3 = Scatter(
    x=allStocks["tickerdate"],
    y=allStocks["gm"],
	line=Line(
        color='rgb(255,0,245)'
    ),
    name='General Motors'
)
trace4 = Scatter(
    x=allStocks["tickerdate"],
    y=allStocks["tm"],
	line=Line(
        color='rgb(186, 27, 218)'
    ),
    name='Toyota'
)
trace5 = Scatter(
    x=allStocks["tickerdate"],
    y=allStocks["jwn"],
	line=Line(
        color='rgb(255,153,51)'
    ),
    name='Nordstrom'
)
trace6 = Scatter(
    x=allStocks["tickerdate"],
    y=allStocks["fox"],
	line=Line(
        color='rgb(0,255,50)'
    ),
    name='Fox'
)
trace7 = Scatter(
    x=allStocks["tickerdate"],
    y=allStocks["media"],
	line=Line(
        color='rgb(255,255,0)'
    ),
    name='Avg. Media Stocks'
)

data =[trace1, trace2, trace3, trace4, trace5, trace6, trace7]

fig = Figure(data=data)
#plot_url = py.plot(fig)
plot_url = plot(fig, auto_open=False)

