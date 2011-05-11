# Copyright 2009, EveryBlock
# This code is released under the GPL.

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
from django.utils.encoding import force_unicode
import urllib

class CachedPageMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        response = None
        if request.method == 'GET' and 'magicflag' not in request.GET and len(request.GET) == 0 and request.path in settings.CACHED_PAGES:
            cache_key = 'page:%s' % urllib.quote(request.path)
            response = HttpResponse(cache.get(cache_key, None))
        try:
            content = response.content
        except (TypeError, AttributeError):
            content = None
        if response is None or not content:
            response = view_func(request, *view_args, **view_kwargs)
        return response
    
    # This is separate to make the flatpage fallback work
    def process_response(self, request, response):
        if 'magicflag' not in request.GET and response['content-type'].startswith('text/html'):
            for bit, template in settings.CACHED_BITS.items():
                response.content = force_unicode(response.content).replace(
                    '<!--CACHED_BIT:%s-->' % bit,
                    loader.render_to_string(template, 
                        context_instance=RequestContext(request)),
                    1
                )
        return response
        
        
