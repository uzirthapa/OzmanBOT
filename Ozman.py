#twitter bot for finding related things on twitter
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener

# read Tweets
import json
import re
import operator
from collections import Counter
from nltk.corpus import stopwords
import string
from nltk import bigrams

import random

consumer_key = "" #please add your own
consumer_secret = "" #please add your own

access_token = "" #please add your own
access_token_secret = "" #please add your own access token

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

file = 'Ozman.json'   #file for collecting and processing tweets

#Remove unnecessary information
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['RT', 'via']


##public_tweets = api.home_timeline()
##for tweet in public_tweets:
##    print (tweet.text)

##results = api.search(q = "#win")
##
##for results in results:
##    print(results.text)
 
class MyListener(StreamListener):
    print("TweetBot 1.0 Loaded....")
    #api.update_status("Hello! Im online! please send me @OzmanBOT a message!")
    print("Listening for data.. @OzmanBOT to talk to BOT")
 
    def on_data(self, data):
        
        try:
            with open(file, 'w') as f:
                f.write(data)
                

            def tokenize(s):
                return tokens_re.findall(s)
             
            def preprocess(s, lowercase=False):
                tokens = tokenize(s)
                if lowercase:
                    tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
                return tokens

            with open(file, 'r') as f:
                for line in f:
                    tweet = json.loads(line)
                #put break for first item
                print(tweet['text'])
                user = tweet['user']['screen_name']
                terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
                print(terms_stop)

                #filter stop words 

            terms_bigram = list(bigrams(terms_stop))
            print(terms_bigram[0][1])
            try:
                word = terms_bigram[0][1] + " or " + twerms_bigram[0][2]
            except:
                word = terms_bigram[0][1]
                

            print(word)
            results = api.search(q = word)
            #for results in results:

            a = results[random.randrange(5)].text
            reply = " ".join(filter(lambda x:x[0]!='@', a.split()))

            api.update_status("@"+ user + " " + reply)
            print("@"+ user + " " + reply)

        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['@OzmanBOT'])
