#! /usr/bin/env python
from twython import TwythonStreamer, Twython
from pymongo import MongoClient
import datetime
import threading
import logging


class TwitterStreamer(TwythonStreamer):
    """
    TwitterStreamer is going to be our Twitter watch.  It streams all data happening on Twitter for the terms
    that we have told it to search for.  It will then save all of those tweets to a Mongodb for our use
    and pleasure.
    """
    def on_success(self, tweet):
        if 'text' in tweet:
            # Get Coordinates
            has_coords = False
            if tweet['coordinates'] or tweet['place']:
                has_coords = True
                logging.info('Tweet has coordinates!')
            # Save Tweet
            tweets.insert(tweet)
            # Save Mentions
            save_mentions(tweet)

    def on_error(self, status_code, data):
        print status_code

    def save_mentions(tweet):
        for mention in tweet['entities']['user_mentions']:
            screen_name = users.find_one({'twitter': mention['screen_name']})
            # If there is a truck, and it is a truck, and the user forgot the coordinates, let's let them know
            if SEND_MESSAGE:
                # Send message to user if not in DEVELOPER_MODE
                logging.info('Sending message to @%s. %s' % (tweet['user']['screen_name'], datetime.datetime.now()))
                if not DEVELOPER_MODE:
                    message_thread = TweetMaker(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET,
                                                tweet['user']['screen_name'])
                    message_thread.start()
            # If no user (mention) was found in our database let's save it
            if not truck:
                users.insert({
                    'twitter': mention['screen_name'],
                    'created': datetime.datetime.utcnow(),
                    'added_by': tweet['user']['screen_name']
                })
                logging.info('Added @%s! %s' % (mention['screen_name'], datetime.datetime.now()))


class TweetMaker(threading.Thread):
    """
    TweetMaker is a self-contained thread for sending a message via Twitter.  It uses whatever access token
    you give it but by default in here we will be using the Twitter account for sending tweets.
    """
    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret, mention):
        threading.Thread.__init__(self)
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        self.mention = mention
        self.twitter = Twython(consumer_key, consumer_secret, access_token_key, access_token_secret)

    def run(self):
        try:
            self.twitter.update_status(status='@%s, thanks for the mention!' % self.mention)
        except:
            logging.error('Failed to send tweet to @%s! %s' % (self.mention, datetime.datetime.now()))

# Are we Developing?
DEVELOPER_MODE = True

# Set up App Keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''

# Start Logging
logging.basicConfig(filename='twitter-scraper.log', level=logging.DEBUG)
logging.info('Started Twitter Scraper!!! %s' % datetime.datetime.now())

# Set up Mongodb
client = MongoClient('mongodb://localhost:12945')

# Set DBs
if DEVELOPER_MODE:
    authenticated = client.dev_tweets.authenticate('scriptUser', 'TwitterTr4ck3r')
    db = client.dev_tweets
else:
    authenticated = client.tweets.authenticate('scriptUser', 'TwitterTr4ck3r')
    db = client.tweets

# Set Collections
tweets = db.tweets
users = db.users

# BEGIN THE STREAM!!!
stream = TwitterStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
# FILTER BY ALL THE THINGS!!!
track_by = ['#twitterscraper']
if DEVELOPER_MODE:
    # Get Worldwide trending topics to filter by for development
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    trending = twitter.get_place_trends(id=1)[0]['trends']
    track_by = []
    for trend in trending:
        track_by.append(trend['name'])
else:
    stream.statuses.filter(track=track_by)