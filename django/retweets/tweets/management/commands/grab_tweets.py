# -*- coding: utf8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand

from ...helpers import getTweets
from ...models import Tweet, ReTweet

class Command(BaseCommand):
    
    def handle(self, **options):
        getter = getTweets(
            settings.TWITTER_USERNAME,
            consumer_key=settings.CONSUMER_KEY,
            consumer_secret=settings.CONSUMER_SECRET,
            access_token_key=settings.ACCESS_TOKEN_KEY,
            access_token_secret=settings.ACCESS_TOKEN_SECRET,
        )
        
        tweets = getter.get_list()
        
        for tweet_json in tweets:
            tweet, created = Tweet.objects.get_or_create(
                pk=tweet_json.id,
                created_at=getter.to_datetime(tweet_json.created_at))
            
            orig_retweet_count = getattr(tweet, 'retweet_count', 0)
            tweet.retweet_count = tweet_json.retweet_count
            tweet.text = tweet_json.text
            if getattr(tweet_json, 'retweeted_status', False):
                author_name = tweet_json.retweeted_status.user.screen_name
            else:
                author_name = tweet_json.user.screen_name
            tweet.screen_name = author_name
            tweet.save()
            if author_name == settings.TWITTER_USERNAME:
                if tweet.retweet_count and tweet.retweet_count > orig_retweet_count:
                    for retweet_json in getter.get_retweets(tweet_json):
                        retweet, created = ReTweet.objects.get_or_create(
                            pk=retweet_json.id,
                            created_at=getter.to_datetime(retweet_json.created_at),
                            tweet_id=tweet
                        )
                        retweet.screen_name = retweet_json.user.screen_name
                        retweet.save()