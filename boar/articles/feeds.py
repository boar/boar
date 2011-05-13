from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed, add_domain
from django.utils.feedgenerator import Atom1Feed
from boar.articles.models import Article, Section, PodcastMetadata, Tag

ITEMS = 30

class ArticlesFeed(Feed):
    title = 'The Boar'
    link = '/'
    description = "The University of Warwick Students' Newspaper"
    description_template = 'articles/feed_articles_description.html'
    feed_type = Atom1Feed
    
    def __init__(self, featured=False, *args, **kwargs):
        self.featured = featured
        return super(ArticlesFeed, self).__init__(*args, **kwargs)
    
    def title(self):
        return u'The Boar%s' % (self.featured and ' (featured)' or '')
    
    def _add_podcast_metadata(self, qs):
        # TODO: 1.2 allows reverse select_related
        items = []
        for item in qs:
            try:
                item.podcast_metadata
            except PodcastMetadata.DoesNotExist:
                item._podcast_metadata_cache = None
            items.append(item)
        return items
    
    def items(self):
        qs = Article.objects.filter(published=True)
        if self.featured:
            qs = qs.filter(featured=True)
        return self._add_podcast_metadata(qs[:ITEMS])
    
    def item_title(self, item):
        return item.title
    
    def item_author_name(self, obj):
        return u', '.join([a.get_full_name() for a in obj.authors.all()])
    
    def item_author_link(self, obj):
        if obj.authors.count() == 1:
            return add_domain(Site.objects.get_current().domain, obj.authors.all()[0].get_absolute_url())
        
    def item_pubdate(self, obj):
        return obj.pub_date
    
    def item_categories(self, obj):
        return [t.name for t in obj.tags.all()]
    
    def item_enclosure_url(self, obj):
        if obj.podcast_metadata:
            return obj.podcast_metadata.podcast.url
    
    def item_enclosure_length(self, obj):
        if obj.podcast_metadata:
            return obj.podcast_metadata.size
        
    item_enclosure_mime_type = "audio/mpeg"
    

class SectionFeed(ArticlesFeed):
    def title(self, obj):
        return u'The Boar: %s%s' % (obj.title, self.featured and ' (featured)' or '')
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def description(self, obj):
        return 'The latest from the %s section.' % obj.title.lower()
    
    def get_object(self, request, slug):
        return Section.objects.get(slug=slug)
    
    def items(self, obj):
        qs = Article.objects.filter(published=True, section=obj)
        if self.featured:
            qs = qs.filter(featured=True)
        return self._add_podcast_metadata(qs[:ITEMS])
        
class TopicFeed(ArticlesFeed):
    def title(self, obj):
        return u'The Boar: %s: %s' % (obj['section'].title, obj['topic'])
        
    def link(self, obj):
        return u'/%s/%s/' % (obj['section'].slug, obj['topic'].slug)
    
    def description(self, obj):
        return u'The latest on "%s" from the %s section.' % (obj['topic'], obj['section'].title.lower())
    
    def get_object(self, request, section_slug, topic_slug):
        return {'topic': Tag.objects.get(slug=topic_slug), 'section': Section.objects.get(slug=section_slug)}
        
    def items(self, obj):
        return self._add_podcast_metadata(
            Article.objects.filter(
                published=True, 
                section=obj['section'], 
                tags__in=[obj['topic']]
            )[:ITEMS]
        )
    

class UserFeed(ArticlesFeed):
    def title(self, obj):
        return u'The Boar: %s' % obj.get_full_name()
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def description(self, obj):
        return u'The latest writing from %s.' % obj.get_full_name()
    
    def get_object(self, request, slug):
        return User.objects.get(username=slug)
    
    def items(self, obj):
        return self._add_podcast_metadata(
            obj.article_set.filter(published=True)[:ITEMS]
        )
        

