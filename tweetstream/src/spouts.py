from __future__ import absolute_import, print_function, unicode_literals

import itertools, time
import tweepy, copy
import Queue, threading
import json

from streamparse.spout import Spout
from time import strftime
#from tweetcred import twitter_credentials

twitter_credentials = {
    "consumer_key"        :  "0o9IMhZjmdEBDcWAejjksiTwa",
    "consumer_secret"     :  "eptk3mRXEK1gSjXu9MXzOlqrR5DGCyE0YRkvM8GR3UblOBSrbg",
    "access_token"        :  "372317379-zs4WZuQ54KBqwLRll4C0A2YhgdzgrfNt8VG4aRek",
    "access_token_secret" :  "0VZK9XEMhut7WSn9RRdJtQ061muHOUpD5nNADoVAizDM9"
}


# Globals
username_list = ['POTUS', 'realDonaldTrump']
follow_list = ['822215679726100480', '25073877']
track_list = ['Trump', 'Obamacare', 'Affordable Care Act']

def auth_get(auth_key):
    if auth_key in twitter_credentials:
        return twitter_credentials[auth_key]
    return None

class TweetStreamListener(tweepy.StreamListener):

    def __init__(self, listener):
        self.listener = listener
        super(self.__class__, self).__init__(listener.tweepy_api())

    def on_status(self, status):
        self.listener.queue().put(status, timeout = 0.01)
        return True

    def on_error(self, status_code):
        return True # keep stream alive

    def on_limit(self, track):
        return True # keep stream alive

class TweetSpout(Spout):

    def initialize(self, stormconf, context):
        self._queue = Queue.Queue(maxsize = 500)

        consumer_key = auth_get("consumer_key")
        consumer_secret = auth_get("consumer_secret")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        if auth_get("access_token") and auth_get("access_token_secret"):
            access_token = auth_get("access_token")
            access_token_secret = auth_get("access_token_secret")
            auth.set_access_token(access_token, access_token_secret)

        self._tweepy_api = tweepy.API(auth)

        # Create the listener for twitter stream
        listener = TweetStreamListener(self)

        # Create the stream and listen for english tweets
        stream = tweepy.Stream(auth, listener, timeout=None)
        stream.filter(follow_list, track_list, async=True)

    def queue(self):
        return self._queue

    def tweepy_api(self):
        return self._tweepy_api

    def next_tuple(self):
        try:
            data = self.queue().get(timeout = 0.1)
            text=data.text
            tweetid=data.id
            tweetdate=data.created_at.strftime('%Y-%m-%d')
            tweettime=data.created_at.strftime('%H:%M:%S')
            userid=data.user.id
            try:
                rt=data.retweeted_status
                retweet_text = rt.text
                retweet_id = rt.id
                retweet_date = rt.created_at.strftime('%Y-%m-%d')
                retweet_time = rt.created_at.strftime('%H:%M:%S')
                retweet_userid=rt.user.id
                retweet_count=rt.retweet_count
                if str(retweet_userid) in follow_list:
                    rtd = {'text':retweet_text, 'tweetid':retweet_id, 'tweetdate':retweet_date, 'tweettime':retweet_time, 'userid':retweet_userid, 'retweet_count':retweet_count, 'retweet_id':None}
                else:
                    rtd = {}
            except:
                retweet_id = None
                rtd = {}
            tweetd = {'text':text, 'tweetid':tweetid, 'tweetdate':tweetdate, 'tweettime':tweettime, 'userid':userid, 'retweet_count':None, 'retweet_id':retweet_id}
            self.queue().task_done()
            self.emit([tweetd, rtd])

        except Queue.Empty:
            self.log("Empty queue exception ")
            time.sleep(0.1)

    def ack(self, tup_id):
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        pass  # if a tuple fails to process, do nothing
