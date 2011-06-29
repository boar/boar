from boar.articles.models import Section, Article, Tag
from boar.common.views import BaseView
from django.contrib.auth.models import User
from django.http import Http404
from django.utils.datastructures import SortedDict
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet, EmptySearchQuerySet

class BaseSearchView(BaseView):
    template = 'search/search.html'
    
    def __init__(self, template=None, load_all=True, form_class=SearchForm, searchqueryset=None):
        super(BaseSearchView, self).__init__()
        
        if searchqueryset is None:
            searchqueryset = SearchQuerySet()
        
        self.load_all = load_all
        self.form_class = form_class
        self.searchqueryset = searchqueryset
        
        if template is not None:
            self.template = template
    
    def get_context(self, request):        
        form = self.build_form(request)
        query = self.get_query(request, form)
        results = self.get_results(request, form, query)
                
        context = super(BaseSearchView, self).get_context(request)
        context.update({
            'form': form,
            'query': query,
            'results': results,
            'facets': self.get_facets(request, results),
        })
        context.update(self.get_extra_context(request, form))
        return context
    
    def get_extra_context(self, request, form):
        return {}
    
    def build_form(self, request):
        """
        Instantiates the form the class should use to process the search query.
        """
        if self.searchqueryset is None:
            return self.form_class(request.GET, load_all=self.load_all)
        
        return self.form_class(request.GET, searchqueryset=self.searchqueryset, load_all=self.load_all)
    
    def get_query(self, request, form):
        """
        Returns the query provided by the user.
        
        Returns an empty string if the query is invalid.
        """
        if form.is_valid():
            return form.cleaned_data['q']
        
        return ''
    
    def get_results(self, request, form, query):
        """
        Fetches the results via the form.
        
        Returns an empty list if there's no query to search with.
        """
        if query:
            return form.search()
        
        return EmptySearchQuerySet()
    
    def get_facets(self, request, results):
        return results.facet_counts()


class SearchView(BaseSearchView):
    pub_date_facets = SortedDict([
        ('[NOW-7DAYS TO NOW]', 'Past week'),
        ('[NOW-1MONTH TO NOW]', 'Past month'),
        ('[NOW-1YEAR TO NOW]', 'Past year'),
    ])
    
    def __init__(self, *args, **kwargs):
        kwargs['searchqueryset'] = SearchQuerySet().facet('section').facet('tag')
        for key in self.pub_date_facets:
            kwargs['searchqueryset'] = kwargs['searchqueryset'].query_facet('pub_date', key)
        super(SearchView, self).__init__(*args, **kwargs)
    
    def get_extra_context(self, request, form):
        if form.cleaned_data['q']:
            users = SearchQuerySet().models(User).load_all().auto_query(
                form.cleaned_data['q']
            )
        else:
            users = EmptySearchQuerySet()
        return {
            'user_results': users,
        }
    
    def get_results(self, request, form, query):
        if query and form.is_valid():
            sqs = self.searchqueryset.auto_query(
                    form.cleaned_data['q']).models(Article).load_all()
            for facet in ('section', 'tag', 'pub_date'):
                key = 'facet_%s' % facet
                if key in request.GET and request.GET[key]:
                    sqs = sqs.narrow('%s:%s' % (facet, request.GET[key]))
            return sqs
        return EmptySearchQuerySet()
    
    def get_facets(self, request, results):
        # FIXME: UURURRGGGHHH
        facet_counts = results.facet_counts()
        if not facet_counts:
            raise Http404('Invalid search, no facets reported.')
        facets = {'selected': {}}
        # pub_date
        facets['fields'] = {'pub_date': []}
        for key, name in self.pub_date_facets.items():
            facets['fields']['pub_date'].append({
                'name': name,
                'key': key,
                'count': facet_counts['queries'].get('pub_date_exact:%s' % key, 0),
            })
        pub_date = request.GET.get('facet_pub_date', None)
        if pub_date and pub_date in self.pub_date_facets:
            facets['selected']['pub_date'] = self.pub_date_facets[pub_date]
        
        # section
        sections = dict((o.slug, o) for o in Section.objects.all())
        facets['fields']['section'] = []
        for key, count in facet_counts['fields'].get('section', []):
            if count > 0:
                facets['fields']['section'].append({
                    'name': sections.get(key, key),
                    'key': key,
                    'count': count,
                })
        section = request.GET.get('facet_section', None)
        if section and section in sections:
            facets['selected']['section'] = sections[section]
        
        # tag
        tag_slugs = []
        facets['fields']['tag'] = []
        for key, count in facet_counts['fields'].get('tag', []):
            if count > 0:
                facets['fields']['tag'].append({
                    'key': key,
                    'name': key,
                    'count': count,
                })
                tag_slugs.append(key)
        tags = dict((t.slug, t) for t in Tag.objects.filter(slug__in=tag_slugs))
        for facet in facets['fields'].get('tag', []):
            try:
                facet['name'] = tags[facet['key']].name
            except KeyError:
                pass
        tag = request.GET.get('facet_tag', None)
        if tag and tag in tags:
            facets['selected']['tag'] = tags[tag]
        
        return facets

