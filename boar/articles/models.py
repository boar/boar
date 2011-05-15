from boar.archive.models import Page
import boar.articles.inlines
from boar.articles.managers import SectionManager, ArticleManager
from boar.uploads.models import Image
import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.text import truncate_words
from ordered_model.models import OrderedModel
from taggit.managers import TaggableManager
from taggit.models import ItemBase, TagBase


class Section(OrderedModel):
    """A group of articles."""
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    menu_item = models.BooleanField(
        default=True,
        help_text='If set, this section will be shown in the menus at the top of the page.')
    colour = models.CharField(blank=True, null=True, max_length=7)
    tag_name = models.CharField(max_length=100, default='Topics', help_text='The plural name given to a tag in this section.')
    editors = models.ManyToManyField(User, blank=True)
    email = models.EmailField(blank=True, null=True)
    
    objects = SectionManager()
    
    def get_absolute_url(self):
        return "/%s/" % self.slug

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        ordering = ['order',]


class Position(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    order = models.IntegerField(blank=True, null=True)
    members = models.ManyToManyField(User, blank=True)
    email = models.EmailField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['order',]


class Tag(TagBase):
    created = models.DateTimeField(editable=False, default=datetime.datetime.now)
    description = models.TextField(blank=True, null=True, help_text="A description of this tag displayed on the tag page.")
    
    class Meta:
        ordering = ['name']
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
    

class TaggedArticle(ItemBase):
    tag = models.ForeignKey(Tag)
    content_object = models.ForeignKey('Article')
    
    @classmethod
    def tags_for(cls, model, instance=None):
        if instance is not None:
            return cls.tag_model().objects.filter(**{
                'taggedarticle__content_object': instance
            })
        return cls.tag_model().objects.filter(**{
            'taggedarticle__content_object__isnull': False
        }).distinct()
    


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(help_text='Used in the URL, generated automatically. Alphanumeric and dashes only.')
    summary = models.TextField(blank=True, null=True, help_text="A sub-heading for the article, designed to grab a reader's attention. Length should be around 100 characters. It should be one sentence with no full stop.")
    image = models.ForeignKey(Image, blank=True, null=True, help_text="The image that represents the article. It will be displayed on the article listing and at the top of the article page.")
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    approved = models.BooleanField(default=True, editable=False)
    published = models.BooleanField(default=False, help_text="Until published, the article will not be listed on the site.")
    featured = models.BooleanField(default=False, help_text="Featured articles will be displayed at the top of the section pages and on the home page.")
    tags = TaggableManager(
        through=TaggedArticle,
        blank=True,
        help_text="Be conservative. Tags should be about the subject of the article, not what is contained inside it. They are used to generate the list of related articles -- they are <em>not</em> search keywords. Specific tags are useful only if you have a specific article you want this article to be related to.<br><br>For example, an article about the Union raising drinks prices may have a quote from the SU president. It should be tagged \"Drinking\" and \"Student's Union\", but not \"President\"."
    )
    authors = models.ManyToManyField(User, blank=True)
    section = models.ForeignKey(Section)
    tone = models.CharField(max_length=25, default='article', help_text='Determines the template used to display the article, and the associated metadata.', choices=(
        ('article', 'Article'),
        ('book', 'Book Review'),
        ('film', 'Film review'),
        ('game', 'Game Review'),
        ('liveblog', 'Live Blog'),
        ('musicalbum', 'Music Album Review'),
        ('musiclive', 'Music Live Review'),
        ('podcast', 'Podcast'),
        ('travel', 'Travel Report'),
        ('url', 'URL'),
    ))
    score = models.IntegerField(blank=True, null=True, choices=(
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ), help_text="The score given for a review.")
    page = models.ForeignKey(Page, null=True, blank=True, related_name='articles', help_text="The page this article is on in the newspaper archive.")
    notes = models.TextField(help_text="Notes for other editors. Not displayed anywhere public.", blank=True, null=True)
    
    objects = ArticleManager()
    
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ('-pub_date',)
        unique_together = (('section', 'slug', 'pub_date'),)
    
    def get_summary(self):
        if self.summary:
            return self.summary
        else:
            return truncate_words(self.body, 15)
    
    def get_absolute_url(self):
        if self.tone == 'url':
            return self.body
        return '/%s/%s/%s/%s/%s/' % (
            self.section.slug, 
            self.pub_date.year, 
            self.pub_date.strftime("%b").lower(), 
            self.pub_date.day, 
            self.slug
        )

    def __unicode__(self):
        return self.title



class Metadata(models.Model):
    def __unicode__(self):
        return unicode(self.article)
    
    class Meta:
        abstract = True


class BookMetadata(Metadata):
    article = models.OneToOneField(Article, related_name='book_metadata', unique=True)
    book_title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100)
    publisher = models.CharField(blank=True, null=True, max_length=100)

    class Meta:
        verbose_name_plural = "book metadata"


class LiveBlogMetadata(Metadata):
    article = models.OneToOneField(Article, related_name='liveblog_metadata', unique=True)
    twitter_username = models.CharField(max_length=255)
    since_tweet_id = models.IntegerField(help_text="The tweet ID that the blog should start after", blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "live blog metadata"


class GameMetadata(Metadata):
    article = models.OneToOneField(Article, related_name='game_metadata', unique=True)
    platform = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "game metadata"


class MusicAlbumMetadata(Metadata):
    article = models.OneToOneField(Article, related_name='musicalbum_metadata', unique=True)
    artist = models.CharField(max_length=100)
    label = models.CharField(blank=True, null=True, max_length=100)
    mbid = models.CharField(blank=True, null=True, max_length=37)
    link = models.URLField(blank=True, null=True)
    album_art = models.ImageField(upload_to="article-metadata/musicalbum/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "music album metadata"


class MusicLiveMetadata(Metadata):
    article = models.OneToOneField(Article, related_name='musiclive_metadata', unique=True)
    artist = models.CharField(max_length=100)
    location = models.CharField(blank=True, null=True, max_length=100)
    date = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "music live metadata"


class PodcastMetadata(Metadata):
    article = models.OneToOneField(Article, related_name='podcast_metadata', unique=True) 
    podcast = models.FileField(upload_to='podcasts/', help_text='Must be in MP3 format')
    size = models.IntegerField(editable=False)
    
    class Meta:
        verbose_name_plural = "podcast metadata"
    
    def save(self, *args, **kwargs):
        self.size = self.podcast.size
        super(PodcastMetadata, self).save(*args, **kwargs)
    

class TravelMetadata(Metadata):
    article = models.OneToOneField(Article, related_name='travel_metadata', unique=True)
    location = models.PointField()
    
    objects = models.GeoManager()
    
    class Meta:
        verbose_name_plural = 'travel metadata'


class Hit(models.Model):
    article = models.ForeignKey(Article)
    date = models.DateTimeField(default=datetime.datetime.now)
    ip_address = models.IPAddressField()
    user = models.ForeignKey(User, blank=True, null=True)

