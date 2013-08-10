import time

def mkdate(tweet):
    return time.strftime('%Y-%m-%d', 
                         time.strptime(tweet.created_at,
                         '%a %b %d %H:%M:%S +0000 %Y'))
