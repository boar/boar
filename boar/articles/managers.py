from boar.cacher.managers import CachingManager, CachingQuerySet
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.db.models.query import QuerySet

class SectionQuerySet(QuerySet):
    def menu_items(self):
        return self.filter(menu_item=True)


class SectionManager(CachingManager):
    def get_query_set(self):
        return SectionQuerySet(self.model)
    
    def menu_items(self):
        return self.get_query_set().menu_items()


class ArticleQuerySet(CachingQuerySet):
    def comment_count(self):
        qn = connection.ops.quote_name
        ctype = ContentType.objects.get_for_model(self.model)
        subquery = """SELECT COUNT(*)
        FROM %(comment_table)s
        WHERE %(comment_table)s.%(content_type_id)s = %%s
        AND %(comment_table)s.%(object_pk)s::int = %(self_table)s.%(pk)s
        AND %(comment_table)s.%(is_public)s = %%s
        """ % { 'comment_table': qn(Comment._meta.db_table),
                'content_type_id': qn('content_type_id'),
                'object_pk': qn('object_pk'),
                'self_table': qn(self.model._meta.db_table),
                'pk': qn(self.model._meta.pk.name),
                'is_public': qn('is_public'),}
        return self.extra(
            select={'comment_count': subquery},
            select_params=(ctype.id, True,),)
    

class ArticleManager(CachingManager):
    def get_query_set(self):
        return ArticleQuerySet(self.model).select_related('section', 'image')
    
    def published(self):
        return self.get_query_set().filter(published=True)
    
    def comment_count(self):
        return self.get_query_set().comment_count()


