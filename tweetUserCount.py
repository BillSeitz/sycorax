#!/usr/bin/env python
"""
tweetUserCount.py by BillSeitz Oct'2014 for seeing who uses a given hashtag most often

launch with `python tweetUserCount.py gamergate`
"""

import os
import sys
import json
from keys import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
import twitter
from random import randint
import time

def load_config(directory):
    filename = os.path.join(directory, "config.json")
    if not os.path.exists(filename):
        raise Exception("Could not find config.json file at %s" % (
                filename
                ))
    data = json.loads(open(filename).read().strip())
    return data

def search(text, since_id = 0): # get tweets matching string
    access_token_key, access_token_secret = config["user_credentials"]["twitter_token"], config["user_credentials"]["twitter_secret"]
    #print 'tokens: ', access_token_key, access_token_secret, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
    api = twitter.Api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, access_token_key, access_token_secret)
    results = api.GetSearch(text, lang='en', count=200, since_id=since_id)
    print 'num results: ', len(results)
    #for result in results:
        #print result, type(result)
        #result = result.__dict__
        #print result, type(result)
    return results

def user_count(tweets): # for batch of tweets, give number by user
    global user_counts
    last_id = 0
    for tweet in tweets:
        if tweet.id > last_id:
            last_id = tweet.id
        user = tweet.user.screen_name
        if user in user_counts.keys():
            user_counts[user] = user_counts[user] + 1
        else:
            user_counts[user] = 1
    print last_id
    return last_id

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s [stringToSearchFor]" % sys.argv[0]
        sys.exit()
    script_directory = 'tweetUserCount'
    directory = os.path.join('/Users/billseitz/documents/djcode/st/sycorax', script_directory)
    config = load_config(directory)
    since_id = 0
    user_counts = {}
    for i in range(0, (15*10)):
        results = search(sys.argv[1], since_id)
        since_id = user_count(results)
        time.sleep(60 * 6)
    print user_counts
