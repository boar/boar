from django.db import models

class UploadManager(models.Manager):
    def published(self):
        return self.get_query_set().annotate(
            article_count=models.Count('article')
        ).filter(article_count__gt=0)

