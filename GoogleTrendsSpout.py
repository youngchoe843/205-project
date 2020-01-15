from streamparse import Spout
from pytrends.request import TrendReq
from Queue import Queue
from threading import Thread, Timer, Event
import pandas
import numpy
import datetime
import os.path

class GoogleTrendsSpout(Spout):
    outputs = ['daily_data']

    def initialize(self, stormconf, context):
        global history_queue, use_history_queue, kw_list, pytrend, monthly_ts, reference_value, refresh_event, refresh_interval

        history_queue = Queue()
        use_history_queue = True
        refresh_event = Event()
        refresh_interval = 4 * 60 * 60  # 4 hours
        refresh_timer = Timer(refresh_interval, lambda refresh_event = refresh_event: refresh_event.set())
        kw_list = ['travel.state.gov','ustraveldocs','ds 160','ds-160','ds160']
        pytrend = TrendReq('dip.berkeley@gmail.com','zxiw<~zFMdXV1pw<SbdGQ.z?UHauT;BrSOb$"y>p5m3|"3#|\W|hg1!cu@!Ikj#lNbP;!.J(m@GGyp15!8?k..N]-SID(lq[Id-Z')
        pytrend.build_payload(kw_list=kw_list, timeframe='all')
        monthly_ts = pytrend.interest_over_time()
        load_normalization_params()

        history_thread = Thread(target=history_producer)
        history_thread.daemon = True
        history_thread.start()

    def next_tuple(self):
        global history_queue, use_history_queue, kw_list, pytrend, monthly_ts, reference_value, refresh_event, refresh_interval

        if use_history_queue or not history_queue.empty():
            daily_data = history_queue.get()
            self.emit(daily_data, daily_data[1][0])
        else:
            new_date = most_recent_date + datetime.timedelta(days=1)
            start_epoch = new_date.replace(day = 1)
            end_epoch = (start_epoch + datetime.timedelta(days = 32)).replace(day = 1) - datetime.timedelta(days = 1)
            timeframe = "{0} {1}".format(start_epoch.isoformat(), end_epoch.isoformat())
            pytrend.build_payload(kw_list=kw_list, timeframe=timeframe)
            ts = pytrend.interest_over_time()
            if ts.index[-1].as_pydatetime() >= new_date:
                ts = ts[ts.index >= new_date.isoformat()]
                pytrend.build_payload(kw_list=kw_list, timeframe='all')
                monthly_ts = pytrend.interest_over_time()
                reference_value = monthly_ts.loc[reference_month][reference_col]

                month_factor = 1.* monthly_ts.loc[start_epoch].as_matrix().max() / reference_value
                daily_ts = 1.* ts.as_matrix() * month_factor
                daily_idx = numpy.array([i.to_pydatetime().date().isoformat() for i in ts.index])
                daily_ts = numpy.concatenate((daily_idx[:,numpy.newaxis], daily_ts), axis=1)
                for daily_ts_index in numpy.arange(daily_ts.shape[0]):
                    daily_data = daily_ts[daily_ts_index, :]
                    self.emit([daily_data], daily_data[0])
                    most_recent_date = datetime.date(*[int(i) for i in daily_data[0].split('-')])
            else:
                refresh_event.wait(refresh_interval)
                refresh_event.clear()

    def ack(self, tup_id):
        pass

    def fail(self, tup_id):
        pass

    def load_normalization_params():
        global kw_list, monthly_ts, reference_month, reference_col

        normalization_params_file = "normalization_params.txt"
        reference_value = monthly_ts.as_matrix()[:-1,:].max()
        if os.path.isfile(normalization_params_file):
            # TODO replace with Spark sequencefile
            params = numpy.loadtxt(normalization_params_file, dtype=str)
            reference_month = params[0]
            reference_col = int(params[1])
        else:
            reference_month = monthly_ts[reference_value==monthly_ts.as_matrix()].index[0].to_pydatetime().date().isoformat()
            reference_col = monthly_ts.as_matrix()[:-1,:].argmax() % len(kw_list)
            # TODO replace with Spark sequencefile
            numpy.savetxt(normalization_params_file, numpy.array([reference_month, str(reference_col)]), fmt="%s")

    def history_producer():
        global history_queue, use_history_queue, monthly_ts, reference_value

        daily_ts = numpy.array([])
        daily_idx = numpy.array([])
        try:
            for index in monthly_ts.index:
                start_epoch = index.date()
                end_epoch = (start_epoch + datetime.timedelta(days = 32)).replace(day = 1) - datetime.timedelta(days = 1)
                timeframe = "{0} {1}".format(start_epoch.isoformat(), end_epoch.isoformat())
                pytrend.build_payload(kw_list=kw_list, timeframe=timeframe)
                ts = pytrend.interest_over_time()
                
                month_factor = 1.* monthly_ts.loc[index].as_matrix().max() / reference_value
                daily_ts = 1.* ts.as_matrix() * month_factor
                daily_idx = numpy.array([i.to_pydatetime().date().isoformat() for i in ts.index])
                daily_ts = numpy.concatenate((daily_idx[:,numpy.newaxis], daily_ts), axis=1)
                for daily_ts_index in numpy.arange(daily_ts.shape[0]):
                    daily_data = daily_ts[daily_ts_index, :]
                    history_queue.put([daily_data])
                    most_recent_date = datetime.date(*[int(i) for i in daily_data[0].split('-')])
        finally:
            use_history_queue = False
