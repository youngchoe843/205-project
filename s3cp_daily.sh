#!/usr/bin/env bash
psql -At -F ' ' -U postgres --command="select * from (select symbol, count(*) from stockhist group by symbol order by symbol) as counts union all select * from (select tickerdate::varchar,price from stockhist order by symbol,tickerdate) as prices;" --dbname=orangetweets|awk '{OFS=",";print "'"'"'" $1 "'"'"'",$2}'|sed -re "s/$/,/"|tr -d '\n'|sed 's/^/[/'|sed 's/$/]/' > ~/daily/stocks.json
~/.local/bin/aws s3 cp --acl public-read ~/daily/stocks.json s3://bas-w205-project/
psql -At -F ' ' -U postgres --command="SELECT * FROM (SELECT source, count(*) FROM approvalratings GROUP BY source ORDER BY source) AS counts UNION ALL SELECT * FROM (SELECT date, rating FROM approvalratings ORDER BY source,date) AS ratings;" --dbname=orangetweets|awk '{OFS=",";print "'"'"'" $1 "'"'"'",$2}'|sed -re "s/$/,/"|tr -d '\n'|sed 's/^/[/'|sed 's/$/]/' > ~/daily/ratings.json
~/.local/bin/aws s3 cp --acl public-read ~/daily/ratings.json s3://bas-w205-project/
psql -At -F ' ' -U postgres --command="SELECT trend_date,kw0,kw1,kw2+kw3+kw4 FROM traveltrends WHERE trend_date>='2017-01-20' ORDER BY trend_date;" --dbname=orangetweets|awk '{OFS=",";print "'"'"'" $1 "'"'"'",$2,$3,$4}'|sed -re "s/$/,/"|tr -d '\n'|sed 's/^/[/'|sed 's/$/]/' > ~/daily/trends.json
~/.local/bin/aws s3 cp --acl public-read ~/daily/trends.json s3://bas-w205-project/
psql -At -F ' ' -U postgres --command="SELECT l.* FROM topiccount AS l JOIN (SELECT topic_id, SUM(topic_count) AS freq FROM topiccount GROUP BY topic_id ORDER BY freq DESC LIMIT 5) AS r ON l.topic_id = r.topic_id WHERE tweet_date >= '2017-04-01' ORDER BY l.topic_id, tweet_date;" --dbname=orangetweets|awk 'BEGIN{c=""}{if (c!=$2){c=$2;print "'"'"'"$2"'"'"'"} print "'"'"'"$1"'"'"'" "," $3 }'|sed -re "s/$/,/"|tr -d '\n'|sed 's/^/[/'|sed 's/$/]/' > ~/daily/topichot.json
~/.local/bin/aws s3 cp --acl public-read ~/daily/topichot.json s3://bas-w205-project/
psql -At -F ' ' -U postgres --command="SELECT tweet_date, topic_id, AVG(sent_score) FROM tweettable WHERE tweet_date >= '2017-04-01' AND topic_id IN ('CHINA','IMMIGRATION','MEDIA','RUSSIA','TAXES') GROUP BY topic_id, tweet_date ORDER BY topic_id, tweet_date;" --dbname=orangetweets|awk 'BEGIN{c=""}{if (c!=$2){c=$2;print "'"'"'"$2"'"'"'"} print "'"'"'"$1"'"'"'" "," $3 }'|sed -re "s/$/,/"|tr -d '\n'|sed 's/^/[/'|sed 's/$/]/' > ~/daily/topichotsent.json
~/.local/bin/aws s3 cp --acl public-read ~/daily/topichotsent.json s3://bas-w205-project/
psql -At -F , -U postgres --command="SELECT ranked.topic_id,tweet_date,rank() OVER (PARTITION BY tweet_date ORDER BY daily_rank, alltime_count DESC) FROM (SELECT *, rank() OVER (PARTITION BY tweet_date ORDER BY topic_count DESC) AS daily_rank FROM topiccount WHERE tweet_date >= '2017-04-01') AS ranked JOIN (SELECT topic_id, SUM(topic_count) AS alltime_count FROM topiccount GROUP BY topic_id) AS summed ON ranked.topic_id = summed.topic_id AND daily_rank <= 5;" --dbname=orangetweets|awk 'BEGIN{FS=",";q="'"'"'"}{if($3<=5){print q $1 q FS q $2 q FS $3 FS}}'|tr -d '\n'|sed 's/^/[/'|sed 's/$/]/' > ~/daily/topichotrank.json
~/.local/bin/aws s3 cp --acl public-read ~/daily/topichotrank.json s3://bas-w205-project/