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
dateSQL= "SELECT max(tickerDate) from stockHist"
cur.execute(dateSQL)
maxDate = cur.fetchone()
today = date.today()
dateAdd = 1

if (maxDate <> None):
    lastDate = maxDate[0]
    #print(today.weekday())
    if(today.weekday() == 5): dateAdd += 1
    if(today.weekday() == 6): dateAdd += 2
    startDate = lastDate + timedelta(days=dateAdd)
else:
    startDate = date(2016, 11, 1)


if (today <= startDate): 
    print("Data is current")
    exit() 
else:
    print("Start Date:", startDate) 
    print("End Date:", today)   


# a list of stock symbols we are looking at:
#   Boeing, Lockheed Martin, General Motors, Toyota, Nordstrom,
# media companies:
#   Twenty-First Century Fox, Inc, CBS, Time Warner,  
#   News Corporation (NWS) (Harper Collins Publishers, Wall Street Journal, etc), 
#   Discovery, Scripps Networks Interactive, Inc. (SNI) (HGTV, DIY Network, Food Network)

stocks = ["BA", "LMT", "GM", "TM", "JWN", "FOX", "CBS", "TWX", "NWS", "DISCA", "SNI"]

# get the lowest stock prices for the date range and stocks we care about

#set our first columns in the dataframe of all stocks using Boeing: it has the correct length
BA = web.DataReader(stocks[0], "yahoo", startDate, today)["Low"]
allStocks = BA
fullLength = len(BA)
#print(allStocks.index.values)
for date in allStocks.index.values:
    miniDate = str(date)[:10]
    cur.execute("INSERT INTO stockHist VALUES (%s, %s, %s)", (miniDate, "BA", allStocks[date]))
    conn.commit()

# add the closing price of each stock to our allStocks dataframe
for stock in stocks[1:]:
    singleStock = web.DataReader(stock, "yahoo", startDate, today)["Low"]
    # get just the values - to make sure we have the correct length
    #stockCol = singleStock.values
    # if we are missing early values, pad them with zeros
    #if (len(stockCol) < fullLength):
	#numRows = (fullLength - len(stockCol))
	#padRec = pd.DataFrame(np.zeros(numRows))
	#stockCol = pd.concat((padRec, pd.DataFrame(stockCol)), 0)
		
    for date in singleStock.index.values:
        miniDate = str(date)[:10]
	cur.execute("INSERT INTO stockHist VALUES (%s, %s, %s)", (miniDate, stock, singleStock[date]))
	conn.commit()
    # reset the date index to Boeing's index
    #stockCol = pd.DataFrame(stockCol).set_index(BA.index)
    # concatenate our data into a single dataframe
    #frames = [allStocks, stockCol]
    #allStocks = pd.concat(frames, axis=1)

