from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.http import HttpResponse

from boar.articles.feeds import ArticlesFeed, SectionFeed, TopicFeed, UserFeed
from boar.articles.models import Section, Article
from boar.articles.views import *
from boar.articles.widgets import MarkItUpWidget
from boar.search.views import SearchView

# Admin things
admin.autodiscover()
admin.site.root_path = '/admin/' # remove for 1.2
admin.site.unregister(FlatPage)

class MDFlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MarkItUpWidget},
    }
    
admin.site.register(FlatPage, MDFlatPageAdmin)

handler500 = 'boar.views.server_error'

urlpatterns = patterns('',
    (r'^$', 'boar.articles.views.home'),
    
    (r'^tests/', include('syndication.tests.urls')),
    
    (r'^accounts/', include('boar.accounts.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^archive/', include('boar.archive.urls')),
    (r'^awards/$', 'boar.awards.views.ceremony_detail'),
    (r'^awards/thanks/$', 'boar.awards.views.ceremony_voted'),
    (r'^bigd/$', 'django.views.generic.simple.redirect_to', {'url': '/a/10j'}),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^contact/', include('boar.contact.urls')),
    (r'^search/', SearchView()),
    url(r'^users/(?P<slug>[\w\.]+)/$', 
        'django.views.generic.list_detail.object_detail', {
            'queryset': User.objects.all(),
            'slug_field': 'username',
            'template_name': 'accounts/user_detail.html',
        }, name="user_detail"),
    url(r'^users/(?P<slug>[\w\.]+)/writing/$', 
        'django.views.generic.list_detail.object_detail', {
            'queryset': User.objects.all(),
            'slug_field': 'username',
            'template_name': 'accounts/user_writing.html',
        }, name="user_writing"),
    url(r'^users/(?P<slug>[\w\.]+)/photography/$', 
        'django.views.generic.list_detail.object_detail', {
            'queryset': User.objects.all(),
            'slug_field': 'username',
            'template_name': 'accounts/user_image_list.html',
        }, name="user_image_list"),
    url(r'^users/(?P<username>[\w\.]+)/photography/(?P<image_id>\d+)/$', 
        'boar.accounts.views.image_detail', 
        name="user_image_detail"),
    url(r'^users/(?P<slug>[\w\.]+)/feed/$', UserFeed(), name='articles_feed_user'),
    
    url(r'^feed/$', ArticlesFeed(), name='articles_feed'),
    url(r'^feed/featured/$', ArticlesFeed(featured=True), name='articles_feed_featured'),
    # TODO: Put these in SectionView
    url(r'^(?P<slug>[-\w]+)/feed/$', SectionFeed(), name='articles_feed_section'),
    url(r'^(?P<slug>[-\w]+)/feed/featured/$', SectionFeed(featured=True), name='articles_feed_section_featured'),
    url(r'^(?P<section_slug>[-\w]+)/(?P<topic_slug>[-\w\+]+)/feed/$',
         TopicFeed(),   
         name='articles_feed_topic'),

    (r'^arts/', include(SectionView(slug='arts').urls)),
    (r'^books/', include(SectionView(slug='books').urls)),
    (r'^comment/', include(CommentSectionView().urls)),
    (r'^features/', include(FeaturesSectionView().urls)),
    (r'^film/', include(FilmSectionView().urls)),
    (r'^games/', include(GamesSectionView().urls)),
    (r'^lifestyle/', include(SectionView(slug='lifestyle').urls)),
    (r'^money/', include(MoneySectionView().urls)),
    (r'^music/', include(MusicSectionView().urls)),
    (r'^news/', include(NewsSectionView().urls)),
    (r'^science/', include(SectionView(slug='science').urls)),
    (r'^sport/', include(SectionView(slug='sport').urls)),
    (r'^travel/', include(TravelSectionView().urls)),
    (r'^tv/', include(SectionView(slug='tv').urls)),
    
    url('^(?P<prefix>%s)/(?P<tiny>\w+)$' % '|'.join(settings.SHORTEN_MODELS.keys()), 'shorturls.views.redirect'),
    url(r'^google875fd42759aaabd6.html$', lambda x: HttpResponse()),
)

if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'^media/(?P<path>.*)$', 
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': 'http://media.theboar.org/images/favicon.ico'}),   
    )
