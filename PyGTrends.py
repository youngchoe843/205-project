from pytrends.request import TrendReq
from time import sleep
import datetime
import itertools
import pandas
import numpy
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(database="orangetweets", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()
kw_list = ['travel.state.gov','ustraveldocs','ds 160','ds-160','ds160']

print("Establishing connection...")
pytrend = TrendReq(<Google account username>,<Google account password>)

print("Obtaining monthly trend...")
pytrend.build_payload(kw_list=kw_list, timeframe='all')
monthly_ts = pytrend.interest_over_time()
reference_value = monthly_ts.as_matrix()[:-1,:].max()
reference_periods = monthly_ts[reference_value==monthly_ts.as_matrix()]
reference_month = reference_periods.index[0].to_pydatetime().date().isoformat()

print("Obtaining daily trends...")
daily_ts = numpy.array([])
daily_idx = numpy.array([])
for index in monthly_ts.index:
    start_epoch = index.date()
    end_epoch = (start_epoch + datetime.timedelta(days = 32)).replace(day = 1) - datetime.timedelta(days = 1)
    timeframe = "{0} {1}".format(start_epoch.isoformat(), end_epoch.isoformat())
    print(timeframe)
    pytrend.build_payload(kw_list=kw_list, timeframe=timeframe)
    ts = pytrend.interest_over_time()

    month_factor = 1.* monthly_ts.loc[index].as_matrix().max() / reference_value
    this_ts = 1.* ts.as_matrix() * month_factor
    daily_ts = this_ts if daily_ts.size == 0 else numpy.concatenate((daily_ts, this_ts))
    this_idx = numpy.array([i.to_pydatetime().date().isoformat() for i in ts.index])
    daily_idx = this_idx if daily_idx.size == 0 else numpy.concatenate((daily_idx, this_idx))
    sleep(1)

daily_ts = numpy.concatenate((daily_idx[:,numpy.newaxis], daily_ts), axis=1)

for ts_point in daily_ts:
    try:
        cur.execute("""SELECT trend_date FROM traveltrends WHERE trend_date=%s""", (ts_point[0],))
        record = cur.fetchall()
        conn.commit()

        if 0 == len(record):
            cur.execute("""INSERT INTO traveltrends (trend_date, kw0, kw1, kw2, kw3, kw4)
                        VALUES (%s, %s, %s, %s, %s, %s)""", ts_point)
        else:
            cur.execute("""UPDATE traveltrends SET kw0=%s, kw1=%s, kw2=%s, kw3=%s, kw4=%s
                        WHERE trend_date=%s""", numpy.concatenate((ts_point[-5:], ts_point[:-5])))
    finally:
        conn.commit()

print("Streaming...")

while True:
    pytrend.build_payload(kw_list=kw_list, timeframe='all')
    monthly_ts = pytrend.interest_over_time()
    index = monthly_ts.index[-1]
    start_epoch = index.date()
    end_epoch = (start_epoch + datetime.timedelta(days = 32)).replace(day = 1) - datetime.timedelta(days = 1)
    timeframe = "{0} {1}".format(start_epoch.isoformat(), end_epoch.isoformat())
    pytrend.build_payload(kw_list=kw_list, timeframe=timeframe)
    ts = pytrend.interest_over_time()

    month_factor = 1.* monthly_ts.loc[index].as_matrix().max() / reference_value
    this_ts = 1.* ts.as_matrix() * month_factor
    this_idx = numpy.array([i.to_pydatetime().date().isoformat() for i in ts.index])
    print("@ %s: fetched up to %s" % (datetime.datetime.now(), this_idx[-1]))
    for ts_point in numpy.concatenate((this_idx[:,numpy.newaxis], this_ts), axis=1):
        try:
            cur.execute("""SELECT trend_date FROM traveltrends WHERE trend_date=%s""", (ts_point[0],))
            record = cur.fetchall()
            conn.commit()

            if 0 == len(record):
                cur.execute("""INSERT INTO traveltrends (trend_date, kw0, kw1, kw2, kw3, kw4)
                            VALUES (%s, %s, %s, %s, %s, %s)""", ts_point)
            else:
                cur.execute("""UPDATE traveltrends SET kw0=%s, kw1=%s, kw2=%s, kw3=%s, kw4=%s
                            WHERE trend_date=%s""", numpy.concatenate((ts_point[-5:], ts_point[:-5])))
        finally:
            conn.commit()

    sleep(6 * 60 * 60)  # 6 hourly update

conn.close()