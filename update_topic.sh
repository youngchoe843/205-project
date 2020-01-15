#!/usr/bin/env bash
while :
do
    time -p nice psql -U postgres --command="UPDATE tweettable SET topic_id = topicname FROM ( SELECT tweet_id, topicname FROM tweettable JOIN tweettopic ON to_tsvector('english', regexp_replace(tweet_text, E'^RT|@\\w{1,15}:?|https?://[\\w\./…]+', '', 'g')) @@ to_tsquery('english', searchphrase) AND topic_id IS NULL LIMIT 1000) AS batch WHERE tweettable.tweet_id = batch.tweet_id;" --dbname=orangetweets &
    sleep 1
    ps -lef | grep '80.*postgres.*UPDATE' | grep -v grep | awk '{print $4}' | xargs renice +10 -p
    wait
    while [ $(psql -At -U postgres --command="SELECT extract(epoch from etl_latency())::integer;" --dbname=orangetweets || 9999) -gt 5 ]; do
        echo throttle
        sleep 5
    done
done
