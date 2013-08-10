import twitter

import datetime
from dateutil.relativedelta import relativedelta
from email.utils import parsedate_tz

from django.conf import settings
from .models import Tweet, ReTweet

class getTweets():
    def __init__(self, username, max_id=None, consumer_key=None,
                 consumer_secret=None, access_token_key=None,
                 access_token_secret=None, since=None):
        self.username = username
        self.max_id = max_id
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
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
        
        kwargs = {
            'screen_name' : self.username,
            'include_rts' : True,
            'exclude_replies' : False,
            'max_id' : self.max_id,
            'count' : 200 # 200 is the max
        }
        self.tweet_list = self.api.GetUserTimeline(**kwargs)
        return self.tweet_list
    
    def get_retweets(self, tweet):
        retweets = []
        for retweet in self.api.GetRetweets(tweet.id):
            retweets.append(retweet)
        return retweets
    
    def to_datetime(self, datestring):
        time_tuple = parsedate_tz(datestring.strip())
        dt = datetime.datetime(*time_tuple[:6])
        return dt - datetime.timedelta(seconds=time_tuple[-1])

class ReTweetsSince(object):
    def __init__(self):
        self.retweets = ReTweet.objects.exclude(screen_name__in=settings.EXCLUDE_LIST)
        self.tweets = Tweet.objects.exclude(screen_name__in=settings.EXCLUDE_LIST)
        self.last_month = datetime.datetime.now() - relativedelta(months=1)
    
    def last_month_retweets(self):
        return self.retweets.filter(created_at__gt=self.last_month)
    
    def last_month_tweets(self):
        return self.tweets.filter(created_at__gt=self.last_month)
        