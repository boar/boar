from haystack import indexes
from haystack import site
from django.contrib.auth.models import User

class UserIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, model_attr='get_full_name')

site.register(User, UserIndex)
