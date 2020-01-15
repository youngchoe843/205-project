#!/usr/bin/env bash
while :
do
    age=$(date -d "-$(curl -s https://dweet.io/get/latest/dweet/for/g81a9HpDiUaCn53zwtooRxkVtvP3XGtOsH2qf0m+GLOxpRNk1CsoQ4MTBP3MNOgy|sed -re 's/.*([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})\.[0-9]{3}Z.*/"\1\2\3 \4:\5:\6" +%s/' | xargs date -d) seconds" +%s)
    if [ $age -gt 600 ]; then
        echo waiting for user...
        (ulimit -f 0; wget -q -t inf -O dweet https://dweet.io/listen/for/dweets/from/g81a9HpDiUaCn53zwtooRxkVtvP3XGtOsH2qf0m+GLOxpRNk1CsoQ4MTBP3MNOgy)
    fi
    for sec in {1..600}
    do
    sleep 1
    jobs -r | grep tweets_fast | wc -l
    if [ $(jobs -r | grep tweets_fast | wc -l) -lt 2 ]; then
        psql -At -F , -U postgres --command="SELECT date_part('epoch',tweet_date+tweet_time),sent_score FROM tweettable_fast;" --dbname=orangetweets|sed -re "s/$/,/"|tr -d '\n'|sed 's/^/[/'|sed 's/$/]/' > ~/tweets_fast.json
        time nice ~/.local/bin/aws s3 cp --acl public-read ~/tweets_fast.json s3://bas-w205-project/ &
    fi
    done
done
