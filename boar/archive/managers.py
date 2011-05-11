from django.db import models
from django.db.models.query import QuerySet

class IssueQuerySet(QuerySet):
    def published(self):
        return self.filter(is_published=True)


class IssueManager(models.Manager):
    def get_query_set(self):
        return IssueQuerySet(self.model)
    
    def published(self):
        return self.get_query_set().published()


