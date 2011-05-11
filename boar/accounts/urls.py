from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'boar.accounts.views.accounts', name='accounts'),
    url(r'^signout/$', 'boar.accounts.views.signout', name='accounts_signout'),
    url(r'^settings/$', 'boar.accounts.views.settings_form', name='accounts_settings'),
    url(r'^mailing-lists/unsubscribe/(?P<user_id>\d+)-(?P<mailing_list_id>\d+)-(?P<token>.+)/$', 
        'boar.mailing_lists.views.unsubscribe', 
        name='accounts_mailing_lists_unsubscribe'),
    url(r'^user-data/$', 'boar.accounts.views.user_data'),
)

