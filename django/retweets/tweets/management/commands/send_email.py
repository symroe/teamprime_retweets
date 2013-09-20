# -*- coding: utf8 -*-
from random import choice

from django.core.management.base import BaseCommand
from django.conf import settings

from templated_email import send_templated_mail

from ...helpers import ReTweetsSince

class Command(BaseCommand):
    
    def handle(self, **options):
        retweets = ReTweetsSince().last_month_retweets()
        screen_names = set(retweets.values_list('screen_name', flat=True))
        
        top_retweets = ReTweetsSince().last_month_tweets().exclude(retweet=None)
        top_retweets = top_retweets.order_by('-retweet_count')[:10]
        
        winner = choice(screen_names)
        
        send_templated_mail(
                template_name='retweets',
                from_email='tweet@talusdesign.co.uk',
                recipient_list=settings.TO_EMAILS,
                context={
                    'screen_names': screen_names,
                    'retweets': retweets[:10],
                    'top_retweets': top_retweets,
                    'winner': winner,
                },
                cc=['sym.roe@talusdesign.co.uk'],
        )