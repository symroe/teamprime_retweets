import twitter

import datetime
import time
from dateutil.relativedelta import relativedelta
from email.utils import parsedate_tz

from utils import mkdir, mkdate, mkpath

class getTweets():
    def __init__(self, username, max_id=None, consumer_key=None,
                 consumer_secret=None, access_token_key=None,
                 access_token_secret=None, tweet_path=None):
        self.username = username
        self.max_id = max_id
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        self.tweet_path = tweet_path
        self._api = None
        self.last_month = datetime.datetime.now() - relativedelta(months=1)
        self.finished = False
    
    @property
    def api(self):
        """
        Used incase we need to re-authenticate at some point.
        """
        if not self._api:
            self._api = twitter.Api(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token_key=self.access_token_key,
                access_token_secret=self.access_token_secret)
        
        return self._api
    
    
    def get_list(self):
        self.tweet_list = self.api.GetUserTimeline(self.username,
                                              exclude_replies=False,
                                              max_id=self.max_id,
                                              count=200)
    
    def parse_tweets(self):
        if not hasattr(self, 'tweet_list'):
            self.get_list()
        self.finished = False
        while not self.finished:
            for tweet in self.tweet_list:
                created_at = self.to_datetime(tweet.created_at)
                print created_at, tweet.text
                if bool(tweet.retweet_count):
                    self.parse_tweet(tweet)
            self.get_list()

    
    def to_datetime(self, datestring):
        time_tuple = parsedate_tz(datestring.strip())
        dt = datetime.datetime(*time_tuple[:6])
        return dt - datetime.timedelta(seconds=time_tuple[-1])
    
    def parse_tweet(self, tweet):
        self.max_id = tweet.id
        created_at = self.to_datetime(tweet.created_at)
        
        if created_at < self.last_month:
            self.finished = True
        
        path = mkpath(self.tweet_path, mkdate(tweet), tweet.id)
        mkdir(path)
        
        f = open(mkpath(path, tweet.id)  + '.json', 'w')
        f.write(tweet.AsJsonString())
        
        retweet_path = mkpath(path, 'retweets')
        mkdir(retweet_path)
        for retweet in self.api.GetRetweets(tweet.id):
            rt_f = open(mkpath(retweet_path, retweet.id)  + '.json', 'w')
            rt_f.write(retweet.AsJsonString())
        

if __name__ == "__main__":
    import settings
    
    getter = getTweets(
        settings.username,
        consumer_key=settings.CONSUMER_KEY,
        consumer_secret=settings.CONSUMER_SECRET,
        access_token_key=settings.ACCESS_TOKEN_KEY,
        access_token_secret=settings.ACCESS_TOKEN_SECRET,
        tweet_path=settings.TWEET_PATH
    )
    
    getter.parse_tweets()