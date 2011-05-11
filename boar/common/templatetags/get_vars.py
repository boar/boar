from django import template

register = template.Library()

@register.simple_tag
def add_get_var(request, key, value):
    get_vars = request.GET.copy()
    get_vars[key] = value
    return get_vars.urlencode()

@register.simple_tag
def remove_get_var(request, key):
    get_vars = request.GET.copy()
    del get_vars[key]
    return get_vars.urlencode()

