import re

from django import template
from django.contrib.comments.models import Comment
from django.core.cache import cache
from django.template.loader import render_to_string
from boar.articles.forms import ArticleArchiveForm
from boar.articles.models import Section, Article, Position, TravelMetadata

register = template.Library()


class GetSectionsNode(template.Node):
    def __init__(self, section=None):
        if section:
            self.section = template.Variable(section)
        else:
            self.section = None
    
    def render(self, context):
        sections = Section.objects.menu_items()
        if self.section:
            section = self.section.resolve(context)
            # We are in a section
            if section:
                for s in sections:
                    if s == section:
                        s.active = True
                        break
        context['sections'] = sections
        return u''

@register.tag
def get_sections(parser, token):
    try:
        section = token.split_contents()[1]
    except IndexError:
        section = None
    return GetSectionsNode(section)


class GetAboutSectionsNode(template.Node):
    def __init__(self, section=None):
        if section:
            self.section = template.Variable(section)
        else:
            self.section = None
    
    def render(self, context):
        sections = Section.objects.menu_items()
        context['sections'] = (
            sections[0:int(len(sections)/2)],
            sections[int(len(sections)/2):]
        )
        return u''

@register.tag
def get_about_sections(parser, token):
    try:
        section = token.split_contents()[1]
    except IndexError:
        section = None
    return GetAboutSectionsNode(section)



@register.inclusion_tag('articles/snippets/sections.html', takes_context=True)
def sections(context):
    if 'section' in context and context['section']:
        section = context['section']
    else:
        section = None
    sections = Section.objects.menu_items()
    if section:
        for s in sections:
            if s == section:
                s.active = True
                break
    return {'sections': sections, 'section': section, 'request': context['request']}

class GetPositionsNode(template.Node):
    def render(self, context):
        context['positions'] = Position.objects.all()
        return u''

@register.tag
def get_positions(parser, token):
    return GetPositionsNode()

@register.filter
def related_to(obj, num):
    return filter(lambda a: a.published, obj.tags.similar_objects())[:int(num)]


class TopicArticlesNode(template.Node):
    def __init__(self, topic, qs=None):
        self.topic = template.Variable(topic)

    def render(self, context):
        if 'articles' in context and context['articles']:
            articles = context['articles']
        else:
            articles = Article.objects.filter(published=True).select_related('section', 'image')
        if 'section' in context:
            articles = articles.filter(section=context['section'])
        if 'exclude' in context:
            articles = articles.exclude(pk__in=context['exclude'])
        
        context["topic_articles"] = articles.filter(tags__in=[self.topic.resolve(context)]).distinct()
        return u''

@register.tag
def topic_articles(parser, token):
    return TopicArticlesNode(*token.split_contents()[1:])


class ArticleSidebarNode(template.Node):
    def render(self, context):
        try:
            return render_to_string('articles/sidebar/%s.html' % context['section'].slug, context)
        except template.TemplateDoesNotExist:
            return render_to_string('articles/sidebar/default.html', context)
        
@register.tag
def article_sidebar(parser, token):
    return ArticleSidebarNode()



class ArticleListBitNode(template.Node):
    left = False
    
    def __init__(self, article):
        self.article = template.Variable(article)
        
    def render(self, context):
        context['a'] = self.article.resolve(context)
        if context['a'].section.slug == 'comment':
            s = 'comment'
        else:
            s = context['a'].tone
        if 'always_left' in context and context['always_left']:
            context['left'] = True
        else:
            if context['a'].image:
                self.left = not self.left
            context['left'] = self.left
        # For the caching thing... EEEUURGGHH
        if 'no_image' not in context:
            context['no_image'] = False
        if 'in_block' not in context:
            context['in_block'] = False
        context['in_section'] = bool(context['section'])
        try:
            return render_to_string('articles/list_bit/%s.html' % s, context)
        except template.TemplateDoesNotExist:
            return render_to_string('articles/list_bit/default.html', context)
        
@register.tag
def article_list_bit(parser, token):
    tokens = token.split_contents()
    return ArticleListBitNode(tokens[1])


@register.inclusion_tag('articles/snippets/stars.html', takes_context=True)
def article_stars(context, score):
    if isinstance(score, int):
        stars = [i <= score for i in range(1, 6)]
    else:
        stars = []
    context.update({'stars': stars, 'score': score})
    return context

@register.inclusion_tag('articles/blocks/section.html', takes_context=True)
def section_block(context, section, heading='3', articles=None):
    if not isinstance(section, Section):
        section = Section.objects.get(slug=section)
    if articles is None:
        articles = Article.objects.filter(published=True)
    if 'exclude' in context:
        articles = articles.exclude(pk__in=context['exclude'])
    articles = articles.filter(section=section)
    context.update({
        'section': section,
        'in_block': True,
        'heading': heading,
        'articles': articles
    })
    return context

@register.inclusion_tag('articles/blocks/popular.html', takes_context=True)
def popular_block(context):
    section = context.get('section', None)
    key = 'popular_articles'
    if section:
        key = '%s:%s' % (key, section.slug)
    d = cache.get(key)
    if d is not None:
        return d
    d = {
        'section': section,
    }
    cache.set(key, d, 600)
    return d

@register.inclusion_tag('articles/blocks/latest_comments.html')
def latest_comments_block():
    return {'comments': Comment.objects.filter(is_public=True, is_removed=False).order_by('-submit_date')}

@register.inclusion_tag('articles/blocks/archive.html')
def archive_block(articles, date, absolute_url):
    if date:
        d = date.strftime('%Y-%b').lower()
    else:
        try:
            d = articles.latest().pub_date.strftime('%Y-%b').lower()
        except Article.DoesNotExist:
            d = None
    return {'form': ArticleArchiveForm({'month': d}, qs=articles),
            'absolute_url': absolute_url,
            'date': date,
            'articles': articles,}

@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

def filmsoc_match(title, group):
    m = re.match(r'(.+?) \((.+?)\)$', title)
    if not m:
        return title
    return m.group(group)

@register.filter_function
def filmsoc_title(title):
    return filmsoc_match(title, 1)

@register.filter_function
def filmsoc_date(title):
    return filmsoc_match(title, 2)

@register.filter_function
def most_commented(articles):
    return articles.comment_count().order_by('-comment_count')

@register.filter_function
def nearby(metadata):
    return TravelMetadata.objects.distance(metadata.location).exclude(pk=metadata.pk).order_by('distance')
