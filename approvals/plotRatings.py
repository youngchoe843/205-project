#import pandas_datareader.data as web
#import pandas_datareader as pdr
import pandas as pd
from datetime import datetime
from datetime import date
from datetime import timedelta
import numpy as np
import re
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from plotly.offline import *
from plotly.graph_objs import *


# get the range of dates for which we want daily stock prices
#Connecting to tcount
conn = psycopg2.connect(database="orangetweets", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()



sqlcommand = "SELECT date, rating FROM approvalratings WHERE source LIKE \'%gallup%\'"
cur.execute(sqlcommand)
results_gall = cur.fetchall()
results_gall = dict(results_gall)

sqlcommand = "SELECT date, rating FROM approvalratings WHERE source LIKE \'%rasmussen%\'"
cur.execute(sqlcommand)
results_ras = cur.fetchall()
results_ras = dict(results_ras)

sqlcommand = "SELECT date, rating FROM approvalratings WHERE source LIKE \'%huffpost%\'"
cur.execute(sqlcommand)
results_hp = cur.fetchall()
results_hp = dict(results_hp)

datelist = pd.date_range(pd.datetime(2017,1,24), pd.datetime.today())
dlist = []
ratelist_gall = []
ratelist_ras = []
ratelist_hp = []
lastval_gall = 0
lastval_ras = 0
lastval_hp = 0
for i in datelist.date :
    monthstr = str(i.month)
    daystr = str(i.day)
    if i.month < 10 :
        monthstr = "0" + monthstr
    if i.day < 10 :
        daystr = "0" + daystr
    tempstr = str(i.year) + monthstr + daystr
    dlist.append(tempstr)
    if tempstr not in results_gall :
	ratelist_gall.append(lastval_gall)
    else :
    	ratelist_gall.append(results_gall[tempstr])
	lastval_gall = results_gall[tempstr]
    if tempstr not in results_ras :
        ratelist_ras.append(lastval_ras)
    else :
        ratelist_ras.append(results_ras[tempstr])
	lastval_ras = results_ras[tempstr]
	lastval_ras = results_ras[tempstr]
    if tempstr not in results_hp :
        ratelist_hp.append(lastval_hp)
    else :
        ratelist_hp.append(results_hp[tempstr])
        lastval_hp = results_hp[tempstr]
        lastval_hip = results_hp[tempstr]

print ("DATES", dlist)
print ("GALLUP", ratelist_gall)
print ("RASMUSS", ratelist_ras)
print ("HUFFP", ratelist_hp)

xvals_lbl = []
for xs in dlist :
    m = re.search(r"([0-9]{4})([0-9]{2})([0-9]{2})", xs)
    tempstr = m.group(2)+"/" + m.group(3)+ "/" + m.group(1)
    xvals_lbl.append(tempstr)

yvals_gall = ratelist_gall
yvals_ras = ratelist_ras
yvals_hp = ratelist_hp
conn.close()


trace1 = Scatter(
    x=xvals_lbl,
    y=yvals_gall,
        line=Line(
        color='rgb(0,116,217)'
    ),
    name='Gallup'
)
trace2 = Scatter(
    x=xvals_lbl,
    y=yvals_ras,
        line=Line(
        color='rgb(217,0,0)'
    ),
    name='Rasmussen'
)
trace3 = Scatter(
    x=xvals_lbl,
    y=yvals_hp,
        line=Line(
        color='rgb(0,217,0)'
    ),
    name='Huffington Post'
)
data = [trace1, trace2, trace3]


layout = Layout(
#    annotations=Annotations([
#        Annotation(
#            x=xvals_lbl,
#            y=yvals_gall,
#            bgcolor='rgb(256, 256, 256)',
#            font=Font(
#                color='rgb(0, 0, 0)',
#                size=10
#            ),
#            text=xvals_lbl
#        ),
#        Annotation(
#            x=xvals_lbl,
#            y=yvals_ras,
#            bgcolor='rgb(0, 256, 256)',
#            font=Font(
#                color='rgb(0, 0, 0)',
#                size=10
#            ),
#            text=xvals_lbl
#        )]),
    title='Donald Trump Approval Ratings',
    yaxis=dict(
        title='Approval Rating (% approve)',
            color='rgb(0,116,217)', range=[0, 100]
    ),
    xaxis=dict(
	autotick=False,
	ticks=xvals_lbl,
	ticklen=4,
	tickwidth=4,
	showticklabels=True
    )
)

fig = Figure(data=data, layout=layout)
plot_url = plot(fig, auto_open=False)
print (plot_url)


