#!/usr/bin/python

import datetime
from dateutil.relativedelta import relativedelta
import itertools
import os
import sys
import time

sys.path = ['/home/ben/Projects', '/home/ben/Projects/django'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'boar.settings'

from graphication import * 
from graphication.wavegraph import WaveGraph
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import *
from boar.accounts.models import UserProfile
from boar.articles.models import Article, Section

for user in User.objects.filter(is_staff=True):
    if user.article_set.count() < 5:
        continue
        
    d = user.article_set.aggregate(Min('pub_date'), Max('pub_date'))
    print d
    min_month = datetime.date(
        d['pub_date__min'].year,
        d['pub_date__min'].month,
        1)
    max_month = datetime.date(
        d['pub_date__max'].year,
        d['pub_date__max'].month,
        1)
        
    series_set = SeriesSet()
    for section in Section.objects.all():
        qs = user.article_set.filter(section=section)
        if qs.count() == 0:
            continue
        months = {}
        month = min_month
        while month <= max_month:
            months[month] = qs.filter(pub_date__gte=month, pub_date__lt=month+relativedelta(months=1)).count()
            month += relativedelta(months=1)
        if len(months.keys()) < 2:
            continue
        print months
        series_set.add_series(Series(str(section), months, section.colour))

    if len(series_set) == 0:
        continue

    # Initialise our Style
    import graphication.examples.lastgraph_css as style

    # Create the output
    output = FileOutput(style)

    # Weeky scale
    scale = AutoWeekDateScale(series_set, short_labels=True)

    # OK, render that.
    wg = WaveGraph(series_set, scale, style, label_curves=True)

    output.add_item(wg, x=0, y=0, width=450, height=150)

    filename = "graphs/user_articles/%s.%s.png" % (user.id, time.time())

    print os.path.join(settings.MEDIA_ROOT, filename)

    output.write("png", os.path.join(settings.MEDIA_ROOT, filename))
    
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.articles_graph = filename
    profile.save()

