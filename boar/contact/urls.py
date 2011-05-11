from django.conf.urls.defaults import *

from boar.contact.views import *

urlpatterns = patterns('',
    url(r'^position/(?P<slug>[-\w]+)/$', 
        ContactPosition(), name='contact_position'),
    url(r'^section/(?P<slug>[-\w]+)/$',
        ContactSection(), name='contact_section'),
    url(r'^user/(?P<slug>\w+)/$', 
        ContactUser(), name='contact_user'),
    url(r'success/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'contact/success.html'}, name='contact_success')
)
    
