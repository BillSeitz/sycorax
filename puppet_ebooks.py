#!/usr/bin/env python
"""
puppet_ebooks.py by BillSeitz Jul'2014 forked from firstWorldStoic.py which was building on LeonardRichardson's sycorax library

see http://webseitz.fluxent.com/wiki/TwitterBot for background

launch with `python puppet_ebooks.py`

Concept*****
* pick at random one of the lists for the puppet_ebooks Twitter account
* grab last 100 tweets from that list
* strip any URLs from tweets, feed rest of content into MarkovChain
* as starting word for new tweet, pick first word from random pick from the incoming tweets
* generate the rest of the new tweet
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

def lists(): # get lists for account
    access_token_key, access_token_secret = config["user_credentials"]["twitter_token"], config["user_credentials"]["twitter_secret"]
    api = twitter.Api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, access_token_key, access_token_secret)
    results = api.GetLists(screen_name=config["user_credentials"]["account"])
    lists = []
    for list in results:
        #print list.id, list.slug, list.member_count
        if list.member_count > 0:
            #list = list.__dict__
            lists.append(list)
    #print results
    return lists
    
def list(lists): # pick 1 list from the list of lists (at random)
    n = len(lists)
    #print n
    from random import randint
    num = randint(0, n-1)
    #print num
    return lists[num]
    
def list_timeline(list): # get the timeline for the selected list
    access_token_key, access_token_secret = config["user_credentials"]["twitter_token"], config["user_credentials"]["twitter_secret"]
    api = twitter.Api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, access_token_key, access_token_secret)
    results = api.GetListTimeline(list.id, list.slug, count = num_tweets)
    #print 'timeline: ', results
    return results

def corpus_assemble(timeline): # assemble trimmed lines of tweets to feed to engine
    import re, random
    if random.random() < .001:
    	keep_handle = True
    else:
    	keep_handle = False
    url_patt = 'http:[^ ]+'
    tweets = []
    for tweet in timeline:
        body = tweet._text
        body = re.sub(url_patt,'', body)
        body = body.replace('|', '')
        body = body.replace('"', '')
        if keep_handle:
            body = body.replace('@', '#')
        #print 'body: ', body
        tweets.append(body)
    #print 'input tweets: ', tweets
    return tweets

def spew(corpus): # feed corpus (set of tweets) into engine, output single tweet
    engin_dir = '/Users/billseitz/documents/djcode/st/wilson/'
    sys.path.append(engin_dir)
    import StaticBotCore
    #print 'in spew'
    for tweet in corpus:
        StaticBotCore.add_to_brain(tweet)
    num_tweets = len(corpus)
    from random import randint
    num = randint(0, num_tweets-1)
    tweet_trigger = corpus[num]
    first_word = tweet_trigger.split()[0]
    #print 'first word: ', first_word
    tweet_out = StaticBotCore.generate_sentence(tweet_trigger) #was first_word
    if len(tweet_out) > 140:
        tweet_out = tweet_out[0:137] + '...'
    #print tweet_out
    return tweet_out
    
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
        api.PostUpdate(line)
        pass
    except twitter.TwitterError, e:
        if e.message != "Status is a duplicate.":
            raise e
    
if __name__ == "__main__":
    script_directory = 'puppet_ebooks'
    directory = os.path.join('/Users/billseitz/documents/djcode/st/sycorax', script_directory)
    config = load_config(directory)
    num_tweets = 200
    lists = lists()
    list_selected = list(lists)
    timeline = list_timeline(list_selected)
    corpus = corpus_assemble(timeline)
    tweet = spew(corpus)
    post(tweet)
    # NEXT STEP - feed to markov chain
    #results = search(search_text)
    #results = trim_results(results)
    #result = pick_result(results)
    #quote = pick_quote(result)
    #tweet = merge_pieces(result, quote)
    #print str(tweet)
    #post(tweet, result["_id"])
