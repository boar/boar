from boar.awards.models import Vote
from django import template

register = template.Library()

@register.filter
def has_voted_for_award(user, pk):
    try:
        pk = int(pk)
    except ValueError:
        return False
    return Vote.objects.filter(user=user, nominee__award__pk=pk).count() > 0