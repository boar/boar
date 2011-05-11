from django import template
from django.conf import settings

register = template.Library()
    
@register.inclusion_tag('facebook_connect/initialize.html')
def initialize_facebook_connect():
    return {'facebook_api_key': settings.FACEBOOK_API_KEY}

@register.simple_tag
def facebook_js():
    return '<script src="http://static.ak.connect.facebook.com/js/api_lib/v0.4/FeatureLoader.js.php" type="text/javascript"></script>'

