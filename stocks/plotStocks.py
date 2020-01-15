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

SQL = "SELECT a.tickerdate, a.price as BA, b.price as LMT, c.price as GM,"
SQL = SQL + " d.price as TM, e.price as JWN, f.price as FOX, AVG(g.price) as MEDIA"
SQL = SQL + " FROM stockhist a, stockhist b, stockhist c, stockhist d, stockhist e," 
SQL = SQL + " stockhist f, stockhist g"
SQL = SQL + " WHERE a.tickerdate = b.tickerdate"
SQL = SQL + " and b.tickerdate = c.tickerdate"
SQL = SQL + " and c.tickerdate = d.tickerdate"
SQL = SQL + " and d.tickerdate = e.tickerdate"
SQL = SQL + " and e.tickerdate = f.tickerdate"
SQL = SQL + " and f.tickerdate = g.tickerdate"
SQL = SQL + " and a.symbol = 'BA'"
SQL = SQL + " and b.symbol = 'LMT'"
SQL = SQL + " and c.symbol = 'GM'"
SQL = SQL + " and d.symbol = 'TM'"
SQL = SQL + " and e.symbol = 'JWN'"
SQL = SQL + " and f.symbol = 'FOX'"
SQL = SQL + " and g.symbol in ('CBS', 'TWX', 'NWS', 'DISCA','SNI')"
SQL = SQL + " GROUP BY 1, 2, 3, 4, 5, 6, 7"
SQL = SQL + " ORDER  BY a.tickerdate"


allStocks = pd.read_sql(SQL, conn)
 
# here are the significant tweet dates for each company
tweetDates = [["Boeing Tweet", date(2016,12,6)], ["Lockheed Martin Tweet", date(2016,12,19)], ["General Motors Tweet", date(2017,1,3)], ["Toyota Tweet", date(2017,1,6)], ["Nordstrom Tweet", date(2017,2,8)]]
stocks = ["BA", "LMT", "GM", "TM", "JWN", "FOX", "CBS", "TWX", "NWS", "DISCA", "SNI"]
tweetDateValues = []

for idx in range(5):
	dateValueSQL = ("SELECT price FROM stockhist WHERE symbol = %(sSymbol)s AND tickerdate = %(sDate)s")
	#dateValueSQL = ' '.join(sqlStrings)
	#curDate = tweetDates[idx][1]
	#print(curDate)
	#result = "SELECT * FROM OE_TAT where convert(date,Time_IST)=?"
	df =  pd.read_sql(dateValueSQL, conn, params = {"sSymbol":stocks[idx] , "sDate":tweetDates[idx][1]})
	#print(dateValueSQL)
	tweetDateValues.append(df["price"])

	#cur.execute(dateValueSQL)
	#tweetDateValues.append(df)
#print(str(tweetDateValues[0].values))
#print(float(tweetDateValues[1].values))
#print(allStocks)
#print(allStocks["BA"])

# plot the stock prices with annotations for important dates
trace1 = Scatter(
    x=allStocks["tickerdate"],
    y=allStocks["ba"],
	line=Line(
        color='rgb(0,116,217)'
    ),
    name='Boeing'
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
layout = Layout(
    annotations=Annotations([
        Annotation(
            x=tweetDates[0][1],
            y=float(tweetDateValues[0].values),
            #ax=52,
            #ay=-108,
            bgcolor='rgb(256, 256, 256)',
            font=Font(
                color='rgb(0, 0, 0)',
                size=14
            ),
            text=tweetDates[0][0]
        ),
        Annotation(
            x=tweetDates[1][1],
            y=float(tweetDateValues[1].values),
            #ax=52,
            #ay=-108,
            bgcolor='rgb(256, 256, 256)',
            font=Font(
                color='rgb(0, 0, 0)',
                size=14
            ),
            text=tweetDates[1][0]
        ),
        Annotation(
            x=tweetDates[2][1],
            y=float(tweetDateValues[2].values),
            #ax=52,
            #ay=-108,
            bgcolor='rgb(256, 256, 256)',
            font=Font(
                color='rgb(0, 0, 0)',
                size=14
            ),
            text=tweetDates[2][0]
        ),
        Annotation(
            x=tweetDates[3][1],
            y=float(tweetDateValues[3].values),
            #ax=52,
            #ay=-108,
            bgcolor='rgb(256, 256, 256)',
            font=Font(
                color='rgb(0, 0, 0)',
                size=14
            ),
            text=tweetDates[3][0]
        )
            ,
        Annotation(
            x=tweetDates[4][1],
            y=float(tweetDateValues[4].values),
            #ax=52,
            #ay=-108,
            bgcolor='rgb(256, 256, 256)',
            font=Font(
                color='rgb(0, 0, 0)',
                size=14
            ),
            text=tweetDates[4][0]
        )
	]),
    title='Stock Prices for Affected Companies',
    yaxis=dict(
        title='Stock Price',
            color='rgb(0,116,217)'
		#range = [-1.0, 1.0]
    )
)

fig = Figure(data=data, layout=layout)
#plot_url = py.plot(fig)
plot_url = plot(fig, auto_open=False)

