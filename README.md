# Orange Tweets

## Introduction

Orange Tweets is an tool for investigating tweets from and about Donald Trump, and potential impacts of those tweets on public sentiment, stock prices, approval ratings. 

Data is gathered from a variety of online sources, including twitter, Yahoo Finance, Rasmussen, Gallup and Google, and compared for potential interactions, shown visually over time in a graphical dashboard. 

Results can be viewed here: https://ocf.io/dip/mids/w205/project/

## Setup

 1. Start EC2 instance running "ami-d4dd4ec3" AMI.
 2. Mount /data partition created in lab 2 or prepare new partition using setup script: `https://s3.amazonaws.com/ucbdatasciencew205/setup_ucb_complete_plus_postgres.sh` and ensure PostgreSQL server is running. (Check using `ps -A | grep postgres`).
 3. Install psycopg, tweepy, pytrends, nltk, plotly, AWS Command Line Interface modules with pip.

```sh
pip install psycopg2==2.6.2
pip install tweepy
pip install pytrends
pip install nltk
pip install plotly
pip install --upgrade --user awscli
```
 4. Download Vader lexicon from python.
```
>>> import nltk
>>> nltk.download('vader_lexicon')
```
 5. Change to `/data` directory

```sh
cd /data
```

 6. Clone the private git repo

```sh
git clone https://github.com/dipidoo/W205-project/
```

 7. Optionally modify the Twitter API credentials and/or filter list in `tweetstream/src/spouts.py`
 8. Optionally modify the Google Trends credential in `pygtrends.py`

## Steps to Run

1. Create orangetweets database, as well as all necessary tables in postgres using `$ python scripts/setup_tweettable.py`
2. Restore db functions and trigger using script scripts/orangetweets.ddl
3. Create cron jobs by executing:  `crontab cronjobs`
   This will kick off collection of stock prices, approval ratings, and topic classification
4. From a separate terminal session, run `python pygtrends.py`. If you are encountering SSL issue, it is due to Google Trends
   not officially supporting API, and may change their protocols at any time. They announced their plan to do so in 2007 when
   Marissa Mayer was still there as the VP who announced so. We have yet to see such API until now. However, it is a valuable
   data source that serves as near-realtime proxy for people's interest in traveling (immigration traffic volume published by
   official sources have 3- to 6-month lag!) unfortunately this requires ad-hoc debugging. Installing these pieces may help as
   a start:

```sh
sudo bash yum install gcc libffi-devel python-devel openssl-devel
pip install requests[security]
pip install pyopenssl ndg-httpsclient pyasn1
```

5. Execute `sparse run` from the tweetstream directory to begin stream processing. `$ cd tweetstream; sparse run`
6. Alternatively, use bash scripting to restart storm if it crashes. `$ until sparse run; do     echo "sparse crashed with exit code $?. Respawning..." >&2;     sleep 1; done`

## Steps to Serve Data

1. Create an S3 bucket with a name of your choice. S3 will serve as your CDN.
2. Go to `https://console.aws.amazon.com/s3/buckets/<your-bucket-name>` substituting `<your-bucket-name>` with your bucket name.
3. Go to 'Permissions' tab and give everyone Read access on Object access, then click 'CORS Configuration' to allow your domain as such

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>https://your.domain.here</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```

4. Use your existing website or create web hosting account.
    * Berkeley Open Computing Facility is a great place to host your website.
      You can even get short url like `https://ocf.io/yourusernamehere`. Cool!
      Visit <https://www.ocf.berkeley.edu/>
    * You can also do this from the same S3 bucket. In the page of step 2, go to
      'Properties' tab and turn on 'Static web hosting'
5. Copy the content of `www` folder into the webroot, including the `js` directory, preserving the tree.
6. Make `~/daily` directory on your EC2 instance:

```sh
mkdir ~/daily
```

7. Install `tmux` or `screen` on your EC2 instance to run the serving daemons. Since yum requires Python 2.6, it's handy
   to create `~/yum` file with the following content, which enables you to call e.g. `sudo bash yum install tmux` from `~`:

```sh
#!/bin/bash
rm /usr/bin/python
ln -s /usr/bin/python2.6 /usr/bin/python
yum "$@"
rm /usr/bin/python
ln -s /usr/bin/python2.7 /usr/bin/python
```

8. Create IAM user on your AWS account and get its security credentials. Follow the instructions at <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html#cli-signup>
   making sure that the IAM user has full access to S3 services.
9. Configure the AWS CLI using the credentials of this newly created account, by running:

```sh
aws configure
```

10. Create multiple sessions using `tmux` or `screen` for each of the following scripts ([^B C] for `tmux`):
    * `trunc_tweettable_fast.sh` which will keep the `tweettable_fast` table performant.
    * `s3cp_tweettable_fast.sh` which will serve [foveated live sentiment view](https://en.wikipedia.org/w/index.php?oldid=768146718),
      putting load on your server only when there are visitors.
