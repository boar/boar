import datetime
import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from tagging.models import Tag

from boar.archive.models import Volume
from boar.articles.models import Article, Section
from boar.articles.tasks import HitTask
from boar.cartoons.models import Cartoon
from boar.common.views import UrlsView

def home(request):
    # Featured articles
    published = Article.objects.filter(published=True)
    news = published.filter(section__slug='news')
    featured = list(news.filter(featured=True).exclude(image=None)[:1])
    if featured:
        featured += list(news.filter(featured=True).exclude(
            pk=featured[0].pk
        )[:2])
    featured_pks = [a.pk for a in featured]
    # 1 or 3 featured articles
    if len(featured) == 2:
        del(featured[1])
    return render_to_response('articles/home.html', {
        'featured': featured,
        'news': news.exclude(pk__in=featured_pks), 
        'latest_issue': Volume.objects.order_by('-order')[0].issues.published()[0],
    }, context_instance=RequestContext(request))


class SectionView(UrlsView):
    section_template = 'articles/sections/default.html'
    topic_template = 'articles/topic_detail.html'
    sub_section_template = 'articles/sections/sub_section.html'
    slug = None
    sub_sections = {}
    
    def __init__(self, slug=None, section_template=None):
        if section_template:
            self.section_template = section_template
        if slug:
            self.slug = slug
        self.urlname_pattern = 'section_%s_%%s' % self.slug
    
    
    ###################
    # Views
    ###################
    
    # Urgh. This needs improving
    def get_index_context(self, date):
        return {}
    
    # This should be abstracted to a view that generates article lists
    def do_index(self, request, year=None, month=None):
        all_articles = self.get_articles()
        date = self.get_date(year, month)
        articles = self.filter_archive(all_articles, date)
        featured = self.get_featured(articles)
        unfeatured_articles = articles.exclude(pk__in=[a.pk for a in featured])
        context = {
            'articles': unfeatured_articles,
            'featured': featured,
            'all_articles': all_articles,
            'topics': self.get_topics_for_articles(articles),
            'date': date,
            'section': self.section,
            'sub_sections': self.get_sub_sections(unfeatured_articles),
        }
        context.update(self.get_index_context(date))
        return self.render(request, self.section_template, context)
    do_index.urlregex = r'^((?P<year>\d{4})/(?P<month>[a-z]{3})/)?$'
    # Todo - create a decorator that will make do_index_archive with separate 
    # regex and URL reverse identifier
    
    def do_topics(self, request, year=None, month=None):
        months = [m.date() for m in Article.objects.filter(published=True, section=self.section).dates('pub_date', 'month')]
        # Specific date or last month
        date = self.get_date(year, month)
        if date is None:
            date = months[-1]
        filters = {'section': self.section}
        filters.update({'pub_date__range': self._filter_range(date)})
        if 'ajax' in request.GET:
            template = 'articles/topic_cloud.html'
        else:
            template = 'articles/topic_list.html'
        return self.render(request, template, {
            'section': self.section,
            'months': months,
            'cloud': Article.tags_manager.cloud(filters=filters),
            'date': date,
        })
    do_topics.urlregex = r'^topics/((?P<year>\d{4})/(?P<month>[a-z]{3})/)?$'
    
    def do_ztopic(self, request, slug, year=None, month=None):
        slug_list = slug.split('+')
        topics = Tag.objects.filter(slug__in=slug_list)
        # __in will ignore missing ones
        if len(topics) != len(slug_list):
            raise Http404("Topic doesn't exist.")
        all_articles = Article.tagged.with_all(topics).filter(published=True, section=self.section).select_related('section', 'image')
        date = self.get_date(year, month)
        articles = self.filter_archive(all_articles, date)
        return self.render(request, self.topic_template, {
            'section': self.section,
            'topics': topics,
            'slug': slug,
            'articles': articles,
            'date': date,
            'all_articles': all_articles,
            'related': sorted(Tag.objects.related_for_model(topics, Article, counts=True), key=lambda x: x.count, reverse=True)[:8],
            'absolute_url': reverse('section_%s_ztopic' % self.section.slug, kwargs={'slug': slug})
        })
    do_ztopic.urlregex = r'^(?P<slug>[-\w\+]+)/((?P<year>\d{4})/(?P<month>[a-z]{3})/)?$'
    
    def do_article(self, request, year, month, day, article_slug):
        date = self.get_date(year, month, day)
        try:
            article = Article.objects.select_related('section', 'image').get( 
                slug=article_slug,
                section=self.section,
                pub_date__range=(
                    datetime.datetime.combine(date, datetime.time.min), 
                    datetime.datetime.combine(date, datetime.time.max)
                ),
            )
            if not article.published and not request.user.is_staff:
                raise Http404('Article does not exist.')
        except Article.DoesNotExist:
            raise Http404('Article does not exist.')
        if not settings.DEBUG:
            HitTask.delay(article=article, date=datetime.datetime.now(), user=request.user, ip_address=request.META['REMOTE_ADDR'])
        context = {
            'article': article,
            'section': self.section,
            # For the topic blocks
            'exclude': [article.pk],
            'preview': not article.published,
        }
        return self.render(request, 'articles/article_detail/%s.html' % article.tone, context)
    do_article.urlregex = r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<article_slug>[-\w]+)/$'
    
    
    ###################
    # Abstract views
    ###################
    
    def sub_section(self, request, slug, year=None, month=None, template=None):
        if template is None:
            template = self.sub_section_template
        sub_section = self.sub_sections[slug]
        all_articles = sub_section['qs'](self.get_articles())
        date = self.get_date(year, month)
        articles = self.filter_archive(all_articles, date)
        return self.render(request, template, {
            'sub_section': sub_section['name'],
            'absolute_url': reverse('section_%s_%s' % (self.section.slug, slug)),
            'articles': articles,
            'all_articles': all_articles,
            'date': date,
            'section': self.section,
            'sub_sections': self.get_sub_sections(self.filter_archive(self.get_articles(), date)),
        })
    
    
    ###################
    # Properties
    ###################
    
    @property
    def section(self):
        if not hasattr(self, '_section'):
            try:
                self._section = Section.objects.get(slug=self.slug)
            except Section.DoesNotExist:
                raise Http404('Section does not exist.')
        return self._section
    
    
    ###################
    # Methods
    ###################
    
    # Once this is done on the default query set, this should not be required.
    def get_articles(self):
        return self.section.article_set.filter(published=True).select_related('section', 'image')        
    
    def get_date(self, year, month, day=None):
        if not month or not year:
            return None
        try:
            if day:
                t = time.strptime(year+month+day, '%Y%b%d')[:3]
            else:
                t = time.strptime(year+month, '%Y%b')[:3]
        except ValueError:
            raise Http404('Invalid date.')
        return datetime.date(*t)
    
    def filter_archive(self, articles, date):
        if date is None:
            return articles
        return articles.filter(pub_date__range= self._filter_range(date))
    
    def _filter_range(self, date):
        """
        Calculate first and last day of month, for use in a date-range lookup.
        """
        first_day = date.replace(day=1)
        if first_day.month == 12:
            last_day = first_day.replace(year=first_day.year + 1, month=1)
        else:
            last_day = first_day.replace(month=first_day.month + 1)
        return (first_day, last_day)
    
    def get_featured(self, articles):
        featured = list(articles.filter(featured=True).exclude(image=None)[:1])
        # Featured articles without images only if we already have one with an 
        # image
        if featured:
            featured += list(articles.filter(featured=True).exclude(
                pk=featured[0].pk
            )[:2])
        # 1 or 3 featured articles
        if len(featured) == 2:
            del(featured[1])
        return featured
    
    def get_topics_for_articles(self, articles):
        try:
            all_topics = Tag.objects.usage_for_queryset(articles, counts=True)
            return sorted(all_topics, key=lambda x: x.count, reverse=True)[:20]
        except Article.DoesNotExist:
            return []
    
    def get_sub_sections(self, articles):
        sub_sections = {}
        for slug, d in self.sub_sections.items():
            sub_sections[slug] = d
            sub_sections[slug]['articles'] = d['qs'](articles)
            sub_sections[slug]['slug'] = slug
        return sub_sections
        
        
        
class CommentSectionView(SectionView):
    slug = 'comment'
    section_template = 'articles/sections/comment/index.html'
    
    def do_cartoon(self, request, year, month, day):
        return self.render(request, 'articles/sections/comment/cartoon.html', {
            'cartoon': get_object_or_404(Cartoon, date=self.get_date(year, month, day)),
            'section': self.section,
        })
    do_cartoon.urlregex = r'^cartoon/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$'
    
    def get_index_context(self, date):
        if date:
            cartoons = Cartoon.objects.filter(date__range=self._filter_range(date))
            try:
                return {'cartoon': cartoons[0]}
            except IndexError:
                return {}
        try:
            return {'cartoon': Cartoon.objects.latest()}
        except Cartoon.DoesNotExist:
            pass
        return {}
    
    def get_featured(self, articles):
        return articles.filter(featured=True)[:3]

class FeaturesSectionView(SectionView):
    slug = 'features'
    section_template = 'articles/sections/features.html'
    
    def get_featured(self, articles):
        featured = list(articles.filter(featured=True).exclude(image=None)[:5])
        # 2 or 5 featured articles
        if len(featured) < 2:
            return []
        if len(featured) < 5:
            return featured[0:2]
        return featured


class FilmSectionView(SectionView):
    slug = 'film'
    section_template = 'articles/sections/film.html'
    
    def get_featured(self, articles):
        featured = list(articles.filter(featured=True).exclude(image=None)[:3])
        if len(featured) < 3:
            return []
        return featured

class GamesSectionView(SectionView):
    slug = 'games'
    section_template = 'articles/sections/games.html'
    
    def get_featured(self, articles):
        featured = list(articles.filter(featured=True).exclude(image=None)[:2])
        # 2 featured articles only
        if len(featured) < 2:
            return []
        return featured


class MoneySectionView(SectionView):
    slug = 'money'
    section_template = 'articles/sections/money.html'
    
    def get_featured(self, articles):
        return articles.filter(featured=True)[:3]


class MusicSectionView(SectionView):
    slug = 'music'
    section_template = 'articles/sections/music/index.html'
    sub_sections = {
        'features': {
            'name': 'Features',
            'qs': lambda qs: qs.exclude(tone='musicalbum').exclude(tone='musiclive'),
        },
        'albums': {
            'name': 'Albums',
            'qs': lambda qs: qs.filter(tone='musicalbum'),
        },
        'live': {
            'name': 'Live',
            'qs': lambda qs: qs.filter(tone='musiclive'),
        },
    }
    
    def do_features(self, request, year=None, month=None):
        return self.sub_section(request, 'features', year, month, template='articles/sections/music/features.html')
    do_features.urlregex = '^features/((?P<year>\d{4})/(?P<month>[a-z]{3})/)?$'
    
    def do_albums(self, request, year=None, month=None):
        return self.sub_section(request, 'albums', year, month, template='articles/sections/music/albums.html')
    do_albums.urlregex = '^albums/((?P<year>\d{4})/(?P<month>[a-z]{3})/)?$'
    
    def do_live(self, request, year=None, month=None):
        return self.sub_section(request, 'live', year, month, template='articles/sections/music/live.html')
    do_live.urlregex = '^live/((?P<year>\d{4})/(?P<month>[a-z]{3})/)?$'
    
    def get_featured(self, articles):
        try:
            featured = list(articles.filter(featured=True, tone='article').exclude(image=None)[:1])
            featured.extend(articles.annotate(
                metadata_count=models.Count('musicalbum_metadata')
            ).filter(
                featured=True,
                tone='musicalbum',
                metadata_count__gt=0
            )[0:2])
            if len(featured) < 3:
                return []
            return featured
        except IndexError:
            return []


class NewsSectionView(SectionView):
    slug = 'news'
    section_template = 'articles/sections/news/index.html'


class TravelSectionView(SectionView):
    slug = 'travel'
    section_template = 'articles/sections/travel.html'
    
    def get_featured(self, articles):
        return list(articles.filter(featured=True).exclude(image=None)[0:1])


