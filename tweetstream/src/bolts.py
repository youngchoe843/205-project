from __future__ import absolute_import, print_function, unicode_literals

from streamparse.bolt import Bolt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import OrderedDict
import psycopg2

# global topic dictionary
topicd = OrderedDict()
topicd['SYRIA'] = ['syria', 'refugee', 'assad']
topicd['CHINA'] = ['china', 'beijing', 'xi']
topicd['ISIS'] = ['isis', 'moab']
topicd['SNL'] = ['snl', 'baldwin']
topicd['HEALTHCARE'] = ['obamacare', 'trumpcare', 'health']
topicd['RUSSIA'] = ['russia', 'moscow', 'manafort', 'kremlin', 'putin']
topicd['BANNON'] = ['bannon']
topicd['NORTH KOREA'] = ['korea']
topicd['TAXES'] = ['tax']
topicd['CLIMATE CHANGE'] = ['climate']
topicd['WIKILEAKS'] = ['wikileaks']
topicd['MELANIA'] = ['melania']
topicd['NATO'] = ['nato']
topicd['RESIST'] = ['resist', 'protest', 'march']
topicd['MUSLIM'] = ['muslim', 'ban', 'islam', 'mosque']
topicd['BERKELEY'] = ['berkeley']
topicd['MARALAGO'] = ['mar-a-lago', 'maralago', 'golf']
topicd['ENVIRONMENT'] = ['environment', 'epa', 'drill', 'coal']
topicd['SCIENCE'] = ['scientist', 'science']
topicd['WALL STREET'] = ['goldman', 'wall street']
topicd['IMMIGRATION'] = ['mexican', 'immigrant', 'immigration', 'foreign', 'ice', 'vetting', 'sanctuary', 'deport']
topicd['ANTHEM'] = ['anthem']
topicd['GORSUCH'] = ['gorsuch', 'supreme']
topicd['CORRPUTION'] = ['corruption', 'emolument', 'scam', 'fraud']
topicd['SPICER'] = ['spicer', 'spicey']
topicd['CONSPIRACY'] = ['conspiracy', 'conspiracies', 'baseless', 'evidence', 'wiretap', 'tap']
topicd['JOBS'] = ['jobs', 'america first']
topicd['APPROVAL'] = ['approval', 'poll']
topicd['MEDIA'] = ['media', 'foxnews', 'cnn', 'msnbc', 'maddow', 'tapper', 'van']
topicd['DEVOS'] = ['devos']
topicd['NEOCON'] = ['neocon']
topicd['ALTRIGHT'] = ['altright']
topicd['BREITBART'] = ['breitbart']
topicd['KUSHNER'] = ['kushner']
topicd['LEGAL'] = ['lawsuit', 'legal', 'impeach', 'constitution', 'scotus', 'crime', 'fbi', 'investigation']
topicd['IVANKA'] = ['ivanka']
topicd['MCCAIN'] = ['mccain']
topicd['PASSOVER'] = ['passover']
topicd['HITLER'] = ['hitler']
topicd['VOTING'] = ['vote', 'voting', 'electoral']
topicd['BUDGET'] = ['budget']
topicd['WOMENS HEALTH'] = ['parenthood', 'reproductive']
topicd['RICE'] = ['rice']


class RTcheckBolt(Bolt):

    def process(self, tup):

        try:
            rtd = tup.values[1]
            if rtd:
                tweetid=rtd['tweetid']
                retweets=rtd['retweet_count']

                conn_string = "dbname='orangetweets' user='postgres' password='pass' host='localhost' port='5432'"
                conn = psycopg2.connect(conn_string)
                cur = conn.cursor()

                check_sql = "SELECT tweet_id FROM tweettable WHERE tweet_id = %s"
                update_sql = "UPDATE tweettable SET retweets = %s WHERE tweet_id = %s"

                try:
                    cur.execute(check_sql, (tweetid,))
                    tweet_exists = cur.fetchone()

                    if tweet_exists:
                        cur.execute(update_sql, (retweets, tweetid))
                        conn.commit()
                        conn.close()
                        # self.emit([{}])
                        self.log('RT count updated.')
                    else:
                        conn.close()
                        self.emit([rtd])
                        self.log("New RT detected.")
                except:
                    None
                    self.log('RT count update failed')
        except:
            self.log('RT check failed')

class TweetTopicBolt(Bolt):

    def process(self, tup):
        try:
            td = tup.values[0]
            text = td['text']
            no_topic = True

            for k in topicd.keys():
                if any(phrase in text.lower() for phrase in topicd[k]):
                    topic = k
                    no_topic = False
                    self.log("Topic found")
                    break
            if no_topic:
                topic = None
                self.log("No topic assigned")
            
            td['topic'] = topic
            self.emit([td])
            
        except:
            td['topic'] = None
            self.emit([td])
            self.log("Topic assignment failed.")


class TweetSentimentBolt(Bolt):

    def process(self, tup):
        try:
            td = tup.values[0]
            text = td['text']  # extract the tweet

            sid = SentimentIntensityAnalyzer()
            try:
                ssdict = sid.polarity_scores(text)
                sentscore = ssdict['compound']
            except:
                sentscore = None

            td['sentscore'] = sentscore
            self.emit([td])
            self.log("Score assigned")
        except:
            self.log("Sentiment score assignment failed.")


class TweetETLBolt(Bolt):

    def process(self, tup):
        td = tup.values[0]
        text=td['text']
        tweetid=td['tweetid']
        date=td['tweetdate']
        time=td['tweettime']
        userid=td['userid']
        replyid=td['retweet_id']
        retweets=td['retweet_count']
        topicid=td['topic']
        sentscore=td['sentscore']

        # do ETL stuff here
        conn_string = "dbname='orangetweets' user='postgres' password='pass' host='localhost' port='5432'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        check_sql = "SELECT tweet_id FROM tweettable WHERE tweet_id = %s"
        insert_sql = """INSERT INTO tweettable (tweet_id,
				        tweet_text,
				        tweet_date,
				        tweet_time,
				        user_id,
				        reply_id,
				        retweets,
				        topic_id,
				        sent_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        # try:
        cur.execute(check_sql, (tweetid,))
        tweet_exists = cur.fetchone()

        if tweet_exists:
            conn.close()
        else:
            cur.execute(insert_sql, (tweetid, text.encode('utf-8'), date, time, userid, replyid, retweets, topicid, sentscore))
            conn.commit()
            conn.close()
            self.log('%s:%s - %s' % (date, time, tweetid))
        # except:
        #     self.log('ETL failed')
