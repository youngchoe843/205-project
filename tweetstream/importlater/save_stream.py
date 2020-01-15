from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import csv
import time
import numpy as np
import json
import os

os.chdir('/data/tweets/')

access_token = "372317379-zs4WZuQ54KBqwLRll4C0A2YhgdzgrfNt8VG4aRek"
access_token_secret = "0VZK9XEMhut7WSn9RRdJtQ061muHOUpD5nNADoVAizDM9"
consumer_key = "0o9IMhZjmdEBDcWAejjksiTwa"
consumer_secret = "eptk3mRXEK1gSjXu9MXzOlqrR5DGCyE0YRkvM8GR3UblOBSrbg"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)
statuslist=[]

class StdOutListener(StreamListener):

    def __init__(self):
        self.tweetids=[]

    def on_data(self, data):
        status=json.loads(data)
#         try:
        try:
            retweets=status[u'retweet_count']
            retweetid=status[u'replied_tweet_id']
        except:
            retweets=0
            retweetid=0

        outtweets = [[status[u'id'], status[u'user'][u'id'], status[u'created_at'], status[u'text'].encode("utf-8"), retweets, retweetid]]
        print(status[u'id'])

        #write the csv
        with open('stream_%s.csv' % status[u'id'], 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["tweetid", "userid", "created_at","text","retweet_count","reply_tweetid"])
            writer.writerows(outtweets)
#         except:
#             pass

        return True

    def on_error(self, status):
        print(status)


userid_list = []
username_list = ['POTUS', 'realDonaldTrump']

for username in username_list:
    user = api.get_user(username)
    userid_list.append(str(user.id))

follow_list = userid_list

track_list = ['Trump travel ban',
              'Trump muslim ban',
              'Trump immigration',
              'Trump executive order',
              'Trump sanctuary',
              'Trump ICE',
              'Trump media',
              'Trump fake news',
              'Trump enemy of the people',
              'Obamacare',
              'Affordable Care Act']

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

stream.filter(follow=follow_list, track=track_list, async=True)
