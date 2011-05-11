try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.
from django import template
from django.shortcuts import render_to_response

def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        return render_to_response('facebook_connect/login_required.html', {},
            template.RequestContext(request))
    return wraps(view_func)(_wrapped_view)
