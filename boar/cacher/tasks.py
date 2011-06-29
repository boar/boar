import datetime
import urllib

from celery.task import PeriodicTask

from django.conf import settings
from django.core.cache import cache
from django.test import Client
from django.utils.encoding import force_unicode, smart_str

class GenerateCachedPagesTask(PeriodicTask):
    run_every = datetime.timedelta(minutes=1)

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        client = Client()
        for url in settings.CACHED_PAGES:
            res = client.get(url+'?magicflag')
            cache_key = 'page:%s' % urllib.quote(url)
            # Assuming cache time comment is at top of page
            res.content = force_unicode(res.content).replace('LIVE', 'CACHED', 1)
            cache.set(cache_key, res.content, 300)

