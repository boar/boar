from django_inlines import inlines

from boar.uploads.models import Image

class QuoteInline(inlines.TemplateInline):
    def get_context(self):
        return {'quote': self.value, 'section': self.context['section']}

inlines.registry.register('quote', QuoteInline)

class NumberInline(inlines.TemplateInline):
    
    def get_context(self):
	num, rest = self.value.split(' ', 1)
	return {'number': num, 'text': rest, 'section': self.context['section']}

inlines.registry.register('number', NumberInline)

class ImageInline(inlines.ModelInline):
    model = Image
    
    def get_context(self):
        context = super(ImageInline, self).get_context()
        if 'height' in self.kwargs:
            height = self.kwargs['height']
        else:
            height = 300
        context['size'] = '417x%s' % height
        return context
        
inlines.registry.register('image', ImageInline)
