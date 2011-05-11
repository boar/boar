from django import template
from django.conf import settings
from boar.uploads.models import Thumbnail

register = template.Library()

def do_thumbnail(parser, token):
    try:
        tag_name, image, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments" % token.contents.split()[0]
    if not (name[0] == name[-1] and name[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's second argument should be in quotes" % tag_name
    
    return ThumbnailNode(image, name[1:-1])
    
    
class ThumbnailNode(template.Node):
    def __init__(self, image, name):
        self.image = template.Variable(image)
        self.name = name
    
    def render(self, context):
        i = self.image.resolve(context)
        try:
            t = Thumbnail.objects.get(image=i, size__name=self.name)
        except Thumbnail.DoesNotExist:
            return u''
        return u'%s%s' % (settings.MEDIA_URL, t.get_path())

register.tag("upload_thumbnail", do_thumbnail)

