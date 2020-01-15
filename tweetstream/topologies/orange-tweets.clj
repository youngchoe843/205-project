(ns orangetweets
  (:use     [streamparse.specs])
  (:gen-class))

(defn orangetweets [options]
   [
    ;; spout configuration
    {"TweetSpout" (python-spout-spec
          ;; topology options passed in
          options
          ;; python class to run
          "spouts.TweetSpout"
          ;; output specification, what named fields will this spout emit?
          ["tweetdict" "rtdict"]
          ;; configuration parameters, can specify multiple or none at all
          )
   }


    ;; bolt configuration
    {"RTcheckBolt" (python-bolt-spec
          ;; topology options pased in
          options
          ;; inputs, where does this bolt receive its tuples from?
          {"TweetSpout" :shuffle}
          ;; python class to run
          "bolts.RTcheckBolt"
          ;; output specification, what named fields will this spout emit?
          ["tweetdict"]
          ;; configuration parameters, can specify multiple or none at all
          :p 1
          )
    "TopicBolt" (python-bolt-spec
          ;; topology options pased in
          options
          ;; inputs, where does this bolt receive its tuples from?
          {"TweetSpout" :shuffle
           "RTcheckBolt" :shuffle}
          ;; python class to run
          "bolts.TweetTopicBolt"
          ;; output specification, what named fields will this spout emit?
          ["tweetdict"]
          ;; configuration parameters, can specify multiple or none at all
          :p 1
          )
    "SentimentBolt" (python-bolt-spec
          ;; topology options pased in
          options
          ;; inputs, where does this bolt receive its tuples from?
          {"TopicBolt" :shuffle}
          ;; python class to run
          "bolts.TweetSentimentBolt"
          ;; output specification, what named fields will this spout emit?
          ["tweetdict"]
          ;; configuration parameters, can specify multiple or none at all
          :p 1
          )
    "ETLBolt" (python-bolt-spec
          ;; topology options pased in
          options
          ;; inputs, where does this bolt receive its tuples from?
          {"SentimentBolt" :shuffle}
          ;; python class to run
          "bolts.TweetETLBolt"
          ;; output specification, what named fields will this spout emit?
          []
          ;; configuration parameters, can specify multiple or none at all
          :p 1
          )
    }
  ]
)