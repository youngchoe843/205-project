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

topTopicsSQL = "SELECT topic_id, sum(topic_count) as ttl FROM topicCount GROUP BY topic_id ORDER BY ttl DESC LIMIT " + str(numTopics)
#print (topTopicsSQL)
ttlCount = pd.read_sql(topTopicsSQL, conn)
#print(ttlCount["topic_id"][0])
pData = []
colors = ['rgb(0,116,217)', 'rgb(255,0,85)', 'rgb(255,0,245)', 'rgb(0,255,50)', 'rgb(255,255,0)', 'rgb(186, 27, 218)', 'rgb(255,153,51)']

for topicIdx in range(numTopics):
	topicName = ''
	topicName = str(ttlCount["topic_id"][topicIdx])
	#print(topicName)
	plotSQL = "SELECT tweet_date, topic_id, topic_count FROM topicCount WHERE topic_id = \'" + topicName + "\'  AND tweet_date > \'2017-04-01\'  ORDER BY tweet_date"
	#print(plotSQL)
	topicCount = pd.read_sql(plotSQL, conn)
	
	
	trace = Scatter(
    	x=topicCount["tweet_date"],
    	y=topicCount["topic_count"],
		line=Line(
    	    color=colors[topicIdx]
   		),
    	name=topicName,
	)


	pData.append(trace)
		
		
layout = dict(
    title= 'Top Tweet Topics with Trump Keyword',

    yaxis=dict(
        #range=[20,30],
        showgrid=True,
        zeroline=True,
        showline=False,
    ),
)		
fig = Figure(data=pData, layout = layout)

#plot_url = py.plot(fig)
plot_url = plot(fig, auto_open=False)