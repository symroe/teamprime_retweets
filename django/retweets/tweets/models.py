from django.db import models

class Tweet(models.Model):
    tweet_id = models.CharField(blank=True, max_length=100, primary_key=True)
    created_at = models.DateTimeField(blank=True)
    retweet_count = models.IntegerField(blank=True, null=True)
    text = models.CharField(blank=True, max_length=150)
    screen_name = models.CharField(blank=True, max_length=100)
    
    def __unicode__(self):
        return self.text

class ReTweet(models.Model):
    tweet_id = models.ForeignKey(Tweet)
    created_at = models.DateTimeField(blank=True)
    screen_name = models.CharField(blank=True, max_length=100)
