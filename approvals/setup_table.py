import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to the database postgres
conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")

#Create the database tcount
try:
    # CREATE DATABASE can't run inside a transaction
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    # change this to orangetweets
    cur.execute("CREATE DATABASE orangetweets")
    cur.close()
    conn.close()
except:
    print "Could not create tcount"


#Connect to tcount to create table inside it
conn = psycopg2.connect(database="orangetweets", user="postgres", password="pass", host="localhost", port="5432")

#Create a Table inside tcount
cur = conn.cursor()
cur.execute('''CREATE TABLE approvalratings (datesource TEXT PRIMARY KEY NOT NULL, source TEXT NOT NULL, date TEXT NOT NULL, rating int NOT NULL);''')
conn.commit()
conn.close()
