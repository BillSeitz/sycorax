#!/usr/bin/env python
"""
firstWorldStoic.py by BillSeitz Apr'2014 building on LeonardRichardson's sycorax library

see http://webseitz.fluxent.com/wiki/TwitterBot for background

launch with `python firstWorldStoic.py`

Concept*****
* search twitter for tweets with "firstworldproblems"
* strip that off (if near end), and any associated hashmark, and all URLs
* simplest: take tweet length, pick randomly from stoic quotes that are short enough to fit, tweet combined line
 * also - make the new tweet a Reply to the captured tweet
* fancier: some logic to match source-tweet with quote, based on keyword, etc.

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

def search(text): # get tweets matching string
    access_token_key, access_token_secret = config["user_credentials"]["twitter_token"], config["user_credentials"]["twitter_secret"]
    #print 'tokens: ', access_token_key, access_token_secret, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
    api = twitter.Api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, access_token_key, access_token_secret)
    results = api.GetSearch(text, lang='en')
    print 'num results: ', len(results)
    results_dicts = []
    for result in results:
        result = result.__dict__
        results_dicts.append(result)
    return results_dicts
    
def trim_results(results): # reduce down to tweets that can work, and strip each to quotable portion
    net_results = []
    import re
    for result in results:
        # drop if too old
        # ????******************************************************
        # strip everything after match
        #print 'starting result: ', result['_text']
        len_result = len(result['_text'])
        pos_match = result['_text'].lower().find(search_text.lower())
        result['_text'] = result['_text'][0:pos_match-1]
        #print 'stripped result: ', result['_text']
        if len(result['_text']) < 10: continue
        if result['_text'][-1] == '#':
            result['_text'] = result['_text'][0:-1]
        # strip any URLs
        url_patt = 'http:[^ ]+'
        result['_text'] = re.sub(url_patt,'', result['_text'])
        result['_text'] = result['_text'].strip()
        if len(result['_text']) < 10: continue
        if result['_text'][-1] not in ['.', '!', '?']:
            result['_text'] = result['_text'] + '.'
        if 10 < len(result['_text']) < 80:
            #print '*** ', result['_text']
            #print str(result['_text']), result['_id']
            net_results.append(result)
    print 'num net results: ', len(net_results)
    return net_results
    
def pick_result(results): # just pick random for now
    num_results = len(results)
    from random import randint
    num = randint(0, num_results-1)
    return results[num]
    
def pick_quote(result): # pick from set of Stoic quotes to match - for now random
    f_path = os.path.join(directory, 'quotes.txt')
    f = open(f_path, 'r')
    lines = f.readlines()
    line_num = randint(0, len(lines)-1)
    line = lines[line_num]
    return line
    
def merge_pieces(result, quote): # glom them together
    line = result['_text'] + ' ' + quote
    if len(line) > 140:
        line = line[0:137] + '...'
    return line
    
def post(line, reply_to=None): # post tweet
    access_token_key, access_token_secret = config["user_credentials"]["twitter_token"], config["user_credentials"]["twitter_secret"]
    #print 'tokens: ', access_token_key, access_token_secret, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
    api = twitter.Api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, access_token_key, access_token_secret)
    # Post the tweet.
    try:
        #print 'will now verify'
        #api.VerifyCredentials()
        #print 'will now post'
        import random
        if random.random() < chance_of_using_reply:
            api.PostUpdate(line, reply_to)
        else:
            api.PostUpdate(line)
        pass
    except twitter.TwitterError, e:
        if e.message != "Status is a duplicate.":
            raise e
    
if __name__ == "__main__":
    script_directory = 'firstWorldStoic'
    search_text = 'firstworldproblem'
    chance_of_using_reply = 0.1
    directory = os.path.join('/Users/billseitz/documents/djcode/st/sycorax', script_directory)
    config = load_config(directory)
    results = search(search_text)
    results = trim_results(results)
    result = pick_result(results)
    quote = pick_quote(result)
    tweet = merge_pieces(result, quote)
    #print str(tweet)
    post(tweet, result["_id"])
