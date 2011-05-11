from django.http import HttpResponse
from django.template import RequestContext, loader, Context

class BaseView(object):
    template = None
    
    def __call__(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)
    
    def get_response(self, request, *args, **kwargs):
        return self.render(request, context=self.get_context(request, *args, **kwargs))
        
    def get_context(self, request, *args, **kwargs):
        return {}
    
    def render(self, request, template=None, context=None):
        if context is None:
            context = {}
        template = self.resolve_template(template or self.template)
        context = self.resolve_context(request, context)
        content = template.render(context)
        return HttpResponse(content)
    
    def resolve_template(self, template):
        "Accepts a template object, path-to-template or list of paths"
        if isinstance(template, (list, tuple)):
            return loader.select_template(template)
        elif isinstance(template, basestring):
            return loader.get_template(template)
        else:
            return template
    
    def resolve_context(self, request, context):
        if isinstance(context, Context):
            return context
        else:
            context_instance = RequestContext(request)
            # Updating the instance like this allows us to use values produced 
            # by TEMPLATE_CONTEXT_PROCESSORS as defaults
            context_instance.update(context)
            return context_instance


class UrlsView(object):
    def render(self, request, template=None, context=None):
        if context is None:
            context = {}
        template = self.resolve_template(template or self.template)
        context = self.resolve_context(request, context)
        content = template.render(context)
        return HttpResponse(content)
    
    def resolve_template(self, template):
        "Accepts a template object, path-to-template or list of paths"
        if isinstance(template, (list, tuple)):
            return loader.select_template(template)
        elif isinstance(template, basestring):
            return loader.get_template(template)
        else:
            return template
    
    def resolve_context(self, request, context):
        if isinstance(context, Context):
            return context
        else:
            context_instance = RequestContext(request)
            # Updating the instance like this allows us to use 
            # TEMPLATE_CONTEXT_PROCESSORS as defaults
            context_instance.update(context)
            return context_instance
    
    def get_urlpatterns(self):
        # Default behaviour is to introspect self for do_* methods
        from django.conf.urls.defaults import url 
        urlpatterns = []
        for method in dir(self):
            if method.startswith('do_'):
                callback = getattr(self, method)
                name = method.replace('do_', '')
                urlname = self.urlname_pattern % name
                urlregex = getattr(callback, 'urlregex', '^%s/$' % name)
                urlpatterns.append(
                    url(urlregex, callback, name=urlname)
                )
        return urlpatterns
    
    def get_urls(self):
        # In Django 1.1 and later you can hook this in to your urlconf
        from django.conf.urls.defaults import patterns
        return patterns('', *self.get_urlpatterns())
    
    @property
    def urls(self):
        return self.get_urls()