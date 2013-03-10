# -*- coding: utf-8 -*-
import glob
from random import choice
import json
from collections import defaultdict

import datetime
from dateutil.relativedelta import relativedelta

last_month = datetime.datetime.now() - relativedelta(months=1)

def mk_user_dict():
    return {
        'count': 0,
        'tweets': []
    }

retweet_people = defaultdict(mk_user_dict)

for tweet_day in glob.glob('tweets/*'):
    folder_date = tweet_day[7:]
    if datetime.datetime.strptime(folder_date, "%Y-%m-%d") < last_month:
        for tweet in glob.glob('tweets/%s/*' % folder_date):
            for retweet in glob.glob('%s/retweets/*' % tweet):
                tweet_json = json.loads(open(retweet, 'r').read())
                name = tweet_json['user']['screen_name']
                if name != "Thayer":
                    retweet_people[name]['count'] = retweet_people[name]['count'] + 1
                    retweet_people[name]['tweets'].append(tweet_json)




people = retweet_people.keys()
people = sorted(people, key=lambda p: retweet_people[p]['count'], reverse=True)

suggested_winner = choice(people)
print "The suggested winner is: %s!" % suggested_winner
print "\n\nHere is the breakdown of retweets since %s:\n\n" % last_month.date()
for person in people:
    print "%s: @%s" % (retweet_people[person]['count'], person)
    for tweet in retweet_people[person]['tweets']:
        print "\t\t", tweet['text']
        print

