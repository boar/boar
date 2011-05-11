from boar.archive.models import Volume
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', {
        'template': 'archive/volume_list.html',
        'extra_context': {'volumes': Volume.objects.order_by('-order')},
    }, name='archive'),
    url(r'^(?P<volume_slug>[-\w]+)/(?P<issue_slug>[-\w]+)/$', 'boar.archive.views.issue', name='archive_issue'),
)
