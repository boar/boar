from haystack import indexes
from haystack import site
from boar.articles.models import Article

class ArticleIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    
    # Faceting fields
    pub_date = indexes.DateField(model_attr='pub_date', faceted=True)
    section = indexes.CharField(null=True, faceted=True)
    tag = indexes.MultiValueField(null=True, faceted=True)
    
    def prepare_section(self, obj):
        return obj.section.slug
    
    def prepare_tag(self, obj):
        return (o.slug for o in obj.tags.all())
    
    def get_queryset(self):
        return super(ArticleIndex, self).get_queryset().exclude(published=False)

site.register(Article, ArticleIndex)
