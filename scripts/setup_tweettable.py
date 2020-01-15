import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")

#Create the Database

try:
    # CREATE DATABASE can't run inside a transaction
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE orangetweets")
    cur.close()
    conn.close()
except:
    print "Could not create orangetweets"

#Connecting to tcount

conn = psycopg2.connect(database="orangetweets", user="postgres", password="pass", host="localhost", port="5432")

#Create a Table
#The first step is to create a cursor.

cur = conn.cursor()


# create tweettable
cur.execute('''CREATE TABLE tweettable
       (tweet_id BIGINT PRIMARY KEY NOT NULL,
       tweet_text TEXT NOT NULL,
       tweet_date DATE NOT NULL,
       tweet_time TIME NOT NULL,
       user_id BIGINT NOT NULL,
       reply_id BIGINT,
       retweets BIGINT,
       topic_id TEXT,
       sent_score REAL NOT NULL);''')
conn.commit()

# create tweettable_fast
cur.execute('''CREATE TABLE tweettable_fast
       (tweet_id BIGINT NOT NULL,
       tweet_text TEXT NOT NULL,
       tweet_date DATE NOT NULL,
       tweet_time TIME NOT NULL,
       user_id BIGINT NOT NULL,
       reply_id BIGINT,
       retweets BIGINT,
       topic_id TEXT,
       sent_score REAL NOT NULL);''')
conn.commit()

# create approvalratings
cur.execute('''CREATE TABLE approvalratings
       (datesource TEXT PRIMARY KEY NOT NULL,
       source TEXT NOT NULL,
       date TEXT NOT NULL,
       rating INT NOT NULL);''')
conn.commit()

# create stockhist
cur.execute('''CREATE TABLE stockhist
       (tickerdate DATE NOT NULL,
       symbol CHAR VARYING(5) NOT NULL,
       price SMALLINT NOT NULL,
       PRIMARY KEY (tickerdate, symbol));''')
conn.commit()

# create topiccount
cur.execute('''CREATE TABLE topiccount
       (tweet_date DATE NOT NULL,
       topic_id TEXT NOT NULL,
       topic_count BIGINT,
       PRIMARY KEY(tweet_date, topic_id));''')
conn.commit()

# create traveltrends
cur.execute('''CREATE TABLE traveltrends
       (trend_date DATE PRIMARY KEY NOT NULL,
       kw0 DOUBLE PRECISION NOT NULL,
       kw1 DOUBLE PRECISION NOT NULL,
       kw2 DOUBLE PRECISION NOT NULL,
       kw3 DOUBLE PRECISION NOT NULL,
       kw4 DOUBLE PRECISION NOT NULL);''')
conn.commit()

# create tweettopic
cur.execute('''CREATE TABLE tweettopic
       (topicname CHAR VARYING(30) NOT NULL,
       searchphrase CHAR VARYING(50) NOT NULL);''')
conn.commit()
