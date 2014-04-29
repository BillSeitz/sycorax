#!/usr/bin/env python
"""
tweet.py by BillSeitz Apr'2014 building on LeonardRichardson's sycorax library

see http://webseitz.fluxent.com/wiki/TwitterBot for background

launch with `python tweet.py PrivateWikiNotebook`
"""

import os
import sys
import json
from keys import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
import twitter
from random import randint

def load_config(directory):
    filename = os.path.join(directory, "config.json")
    if not os.path.exists(filename):
        raise Exception("Could not find config.json file at %s" % (
                filename
                ))
    data = json.loads(open(filename).read().strip())
    return data

def pick_stream():
    #stream = 'markov.txt'
    stream_num = randint(0, len(config["streams"])-1)
    stream = config["streams"][stream_num]
    print 'stream: ', stream
    return stream

def line_to_tweet(stream):
    #line = 'Became PbWorks.'
    f_path = os.path.join(directory, stream)
    f = open(f_path, 'r')
    lines = f.readlines()
    line_num = randint(0, len(lines)-1)
    line = lines[line_num]
    line = line + ' \\' + stream[0]
    print 'line: ', line
    return line
    
def post(line):
    access_token_key, access_token_secret = config["user_credentials"]["twitter_token"], config["user_credentials"]["twitter_secret"]
    #print 'tokens: ', access_token_key, access_token_secret, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
    api = twitter.Api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, access_token_key, access_token_secret)
    # Post the tweet.
    try:
    	#print 'will now verify'
    	#api.VerifyCredentials()
    	#print 'will now post'
        api.PostUpdate(line)
        pass
    except twitter.TwitterError, e:
        if e.message != "Status is a duplicate.":
            raise e
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s [script directory]" % sys.argv[0]
        sys.exit()
    script_directory = sys.argv[1]
    directory = os.path.join('/Users/billseitz/documents/djcode/st/sycorax', script_directory)
    config = load_config(directory)
    stream = pick_stream()
    tweet = line_to_tweet(stream)
    post(tweet)
    