from django.contrib import admin
from models import Tweet, ReTweet

class TweetAdmin(admin.ModelAdmin):
    list_display = ['screen_name', 'retweet_count', 'text', 'created_at']

class ReTweetAdmin(admin.ModelAdmin):
    list_display = ['screen_name', 'created_at', 'tweet_id']

admin.site.register(Tweet, TweetAdmin)
admin.site.register(ReTweet, ReTweetAdmin)