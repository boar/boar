from django.conf import settings

def google_maps_api_key(request):
    return {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}

def default_section(request):
    return {'section': ''}
