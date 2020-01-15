#!/usr/bin/env bash
while :
do
    sleep 1
    time -p nice psql -U postgres --command="DELETE FROM tweettable_fast WHERE tweet_date < current_date OR tweet_time < current_time - interval '00:01';" --dbname=orangetweets || break
done
