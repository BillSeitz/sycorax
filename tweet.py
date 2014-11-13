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

def expandWikiWord(text):
    """
    This is a generalization of page.split_title for 
    ExpandingWikiWords - by BillSeitz
    
    @param text: text to expand
    @rtype: unicode
    @return: text split into space separated words
    """
    import re
    chars_upper = u"\u0041\u0042\u0043\u0044\u0045\u0046\u0047\u0048\u0049\u004a\u004b\u004c\u004d\u004e\u004f\u0050\u0051\u0052\u0053\u0054\u0055\u0056\u0057\u0058\u0059\u005a\u00c0\u00c1\u00c2\u00c3\u00c4\u00c5\u00c6\u00c7\u00c8\u00c9\u00ca\u00cb\u00cc\u00cd\u00ce\u00cf\u00d0\u00d1\u00d2\u00d3\u00d4\u00d5\u00d6\u00d8\u00d9\u00da\u00db\u00dc\u00dd\u00de\u0100\u0102\u0104\u0106\u0108\u010a\u010c\u010e\u0110\u0112\u0114\u0116\u0118\u011a\u011c\u011e\u0120\u0122\u0124\u0126\u0128\u012a\u012c\u012e\u0130\u0132\u0134\u0136\u0139\u013b\u013d\u013f\u0141\u0143\u0145\u0147\u014a\u014c\u014e\u0150\u0152\u0154\u0156\u0158\u015a\u015c\u015e\u0160\u0162\u0164\u0166\u0168\u016a\u016c\u016e\u0170\u0172\u0174\u0176\u0178\u0179\u017b\u017d\u0181\u0182\u0184\u0186\u0187\u0189\u018a\u018b\u018e\u018f\u0190\u0191\u0193\u0194\u0196\u0197\u0198\u019c\u019d\u019f\u01a0\u01a2\u01a4\u01a6\u01a7\u01a9\u01ac\u01ae\u01af\u01b1\u01b2\u01b3\u01b5\u01b7\u01b8\u01bc\u01c4\u01c7\u01ca\u01cd\u01cf\u01d1\u01d3\u01d5\u01d7\u01d9\u01db\u01de\u01e0\u01e2\u01e4\u01e6\u01e8\u01ea\u01ec\u01ee\u01f1\u01f4\u01f6\u01f7\u01f8\u01fa\u01fc\u01fe\u0200\u0202\u0204\u0206\u0208\u020a\u020c\u020e\u0210\u0212\u0214\u0216\u0218\u021a\u021c\u021e\u0220\u0222\u0224\u0226\u0228\u022a\u022c\u022e\u0230\u0232\u0386\u0388\u0389\u038a\u038c\u038e\u038f\u0391\u0392\u0393\u0394\u0395\u0396\u0397\u0398\u0399\u039a\u039b\u039c\u039d\u039e\u039f\u03a0\u03a1\u03a3\u03a4\u03a5\u03a6\u03a7\u03a8\u03a9\u03aa\u03ab\u03d2\u03d3\u03d4\u03d8\u03da\u03dc\u03de\u03e0\u03e2\u03e4\u03e6\u03e8\u03ea\u03ec\u03ee\u03f4\u0400\u0401\u0402\u0403\u0404\u0405\u0406\u0407\u0408\u0409\u040a\u040b\u040c\u040d\u040e\u040f\u0410\u0411\u0412\u0413\u0414\u0415\u0416\u0417\u0418\u0419\u041a\u041b\u041c\u041d\u041e\u041f\u0420\u0421\u0422\u0423\u0424\u0425\u0426\u0427\u0428\u0429\u042a\u042b\u042c\u042d\u042e\u042f\u0460\u0462\u0464\u0466\u0468\u046a\u046c\u046e\u0470\u0472\u0474\u0476\u0478\u047a\u047c\u047e\u0480\u048a\u048c\u048e\u0490\u0492\u0494\u0496\u0498\u049a\u049c\u049e\u04a0\u04a2\u04a4\u04a6\u04a8\u04aa\u04ac\u04ae\u04b0\u04b2\u04b4\u04b6\u04b8\u04ba\u04bc\u04be\u04c0\u04c1\u04c3\u04c5\u04c7\u04c9\u04cb\u04cd\u04d0\u04d2\u04d4\u04d6\u04d8\u04da\u04dc\u04de\u04e0\u04e2\u04e4\u04e6\u04e8\u04ea\u04ec\u04ee\u04f0\u04f2\u04f4\u04f8\u0500\u0502\u0504\u0506\u0508\u050a\u050c\u050e\u0531\u0532\u0533\u0534\u0535\u0536\u0537\u0538\u0539\u053a\u053b\u053c\u053d\u053e\u053f\u0540\u0541\u0542\u0543\u0544\u0545\u0546\u0547\u0548\u0549\u054a\u054b\u054c\u054d\u054e\u054f\u0550\u0551\u0552\u0553\u0554\u0555\u0556\u10a0\u10a1\u10a2\u10a3\u10a4\u10a5\u10a6\u10a7\u10a8\u10a9\u10aa\u10ab\u10ac\u10ad\u10ae\u10af\u10b0\u10b1\u10b2\u10b3\u10b4\u10b5\u10b6\u10b7\u10b8\u10b9\u10ba\u10bb\u10bc\u10bd\u10be\u10bf\u10c0\u10c1\u10c2\u10c3\u10c4\u10c5\u1e00\u1e02\u1e04\u1e06\u1e08\u1e0a\u1e0c\u1e0e\u1e10\u1e12\u1e14\u1e16\u1e18\u1e1a\u1e1c\u1e1e\u1e20\u1e22\u1e24\u1e26\u1e28\u1e2a\u1e2c\u1e2e\u1e30\u1e32\u1e34\u1e36\u1e38\u1e3a\u1e3c\u1e3e\u1e40\u1e42\u1e44\u1e46\u1e48\u1e4a\u1e4c\u1e4e\u1e50\u1e52\u1e54\u1e56\u1e58\u1e5a\u1e5c\u1e5e\u1e60\u1e62\u1e64\u1e66\u1e68\u1e6a\u1e6c\u1e6e\u1e70\u1e72\u1e74\u1e76\u1e78\u1e7a\u1e7c\u1e7e\u1e80\u1e82\u1e84\u1e86\u1e88\u1e8a\u1e8c\u1e8e\u1e90\u1e92\u1e94\u1ea0\u1ea2\u1ea4\u1ea6\u1ea8\u1eaa\u1eac\u1eae\u1eb0\u1eb2\u1eb4\u1eb6\u1eb8\u1eba\u1ebc\u1ebe\u1ec0\u1ec2\u1ec4\u1ec6\u1ec8\u1eca\u1ecc\u1ece\u1ed0\u1ed2\u1ed4\u1ed6\u1ed8\u1eda\u1edc\u1ede\u1ee0\u1ee2\u1ee4\u1ee6\u1ee8\u1eea\u1eec\u1eee\u1ef0\u1ef2\u1ef4\u1ef6\u1ef8\u1f08\u1f09\u1f0a\u1f0b\u1f0c\u1f0d\u1f0e\u1f0f\u1f18\u1f19\u1f1a\u1f1b\u1f1c\u1f1d\u1f28\u1f29\u1f2a\u1f2b\u1f2c\u1f2d\u1f2e\u1f2f\u1f38\u1f39\u1f3a\u1f3b\u1f3c\u1f3d\u1f3e\u1f3f\u1f48\u1f49\u1f4a\u1f4b\u1f4c\u1f4d\u1f59\u1f5b\u1f5d\u1f5f\u1f68\u1f69\u1f6a\u1f6b\u1f6c\u1f6d\u1f6e\u1f6f\u1fb8\u1fb9\u1fba\u1fbb\u1fc8\u1fc9\u1fca\u1fcb\u1fd8\u1fd9\u1fda\u1fdb\u1fe8\u1fe9\u1fea\u1feb\u1fec\u1ff8\u1ff9\u1ffa\u1ffb\u2102\u2107\u210b\u210c\u210d\u2110\u2111\u2112\u2115\u2119\u211a\u211b\u211c\u211d\u2124\u2126\u2128\u212a\u212b\u212c\u212d\u2130\u2131\u2133\u213e\u213f\u2145\uff21\uff22\uff23\uff24\uff25\uff26\uff27\uff28\uff29\uff2a\uff2b\uff2c\uff2d\uff2e\uff2f\uff30\uff31\uff32\uff33\uff34\uff35\uff36\uff37\uff38\uff39\uff3a"
    split_caps = re.compile('([%s])' % (chars_upper), re.UNICODE)
    # look for the end of words and the start of a new word,
    # and insert a space there
    if len(text) <= 8: return text
    splitted = split_caps.sub(r' \1', text).strip()
    return splitted

def tweet_page_lines(stream):
    import time
    page_url = stream[0:-4] #strip .txt
    page_name = expandWikiWord(page_url)
    line = 'w0/ %s http://webseitz.fluxent.com/wiki/%s' % (page_name, page_url)
    first_id = post(line).id # need to capture the ID for this, so rest can be replies
    f_path = os.path.join(directory, stream)
    f = open(f_path, 'r')
    lines = f.readlines()
    i = 0
    for line in lines:
        line = line.translate(None, '*') 
        line = line.strip()
        if len(line) > 2:
            i = i+1
            line = 'w%d/ %s' % (i, line)
            if len(line) > 137:
                line = line[0:133] + '...'
            time.sleep(30)
            print line
            post(line, first_id)

def line_to_tweet(stream):
    #line = 'Became PbWorks.'
    f_path = os.path.join(directory, stream)
    f = open(f_path, 'r')
    lines = f.readlines()
    line_num = randint(0, len(lines)-1)
    line = lines[line_num]
    if len(line) > 137:
        line = line[0:133] + '...'
    line = line + ' \\' + stream[0]
    print 'line: ', line
    return line
    
def post(line, reply_to = None):
    access_token_key, access_token_secret = config["user_credentials"]["twitter_token"], config["user_credentials"]["twitter_secret"]
    #print 'tokens: ', access_token_key, access_token_secret, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
    api = twitter.Api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, access_token_key, access_token_secret)
    # Post the tweet.
    try:
        #print 'will now verify'
        #api.VerifyCredentials()
        #print 'will now post'
        return api.PostUpdate(line, reply_to)
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
    if script_directory == 'wikiLogPageStorm':
        tweet_page_lines(stream)
    else:
        tweet = line_to_tweet(stream)
        post(tweet)
