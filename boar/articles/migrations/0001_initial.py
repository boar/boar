
from south.db import db
from django.db import models
from boar.articles.models import *

class Migration:
    depends_on = ('uploads', '0001_initial'),
    
    def forwards(self, orm):
        
        # Adding model 'TopicMetadata'
        db.create_table('articles_topicmetadata', (
            ('description', models.TextField(null=True, blank=True)),
            ('link_url', models.URLField(null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('topic', models.OneToOneField(orm['tagging.Tag'], related_name='metadata', unique=True)),
            ('link_name', models.CharField(max_length=100, null=True, blank=True)),
            ('image', models.ForeignKey(orm['uploads.Image'], null=True, blank=True)),
        ))
        db.send_create_signal('articles', ['TopicMetadata'])
        
        # Adding model 'Section'
        db.create_table('articles_section', (
            ('menu_item', models.BooleanField(default=True)),
            ('title', models.CharField(max_length=100)),
            ('colour', models.CharField(max_length=7, null=True, blank=True)),
            ('order', models.IntegerField(null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField()),
        ))
        db.send_create_signal('articles', ['Section'])
        
        # Adding model 'Article'
        db.create_table('articles_article', (
            ('body', models.TextField()),
            ('title', models.CharField(max_length=100)),
            ('image', models.ForeignKey(orm['uploads.Image'], null=True, blank=True)),
            ('tags', TagField()),
            ('section', models.ForeignKey(orm.Section, null=True, blank=True)),
            ('summary', models.TextField(null=True, blank=True)),
            ('featured', models.BooleanField(default=False)),
            ('score', models.IntegerField(null=True, blank=True)),
            ('published', models.BooleanField(default=False)),
            ('id', models.AutoField(primary_key=True)),
            ('pub_date', models.DateTimeField(default=datetime.datetime.now)),
            ('slug', models.SlugField()),
            ('approved', models.BooleanField(default=False)),
        ))
        db.send_create_signal('articles', ['Article'])
        
        
        
        # Adding ManyToManyField 'Article.authors'
        db.create_table('articles_article_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(Article, null=False)),
            ('user', models.ForeignKey(User, null=False))
        ))
        
        # Creating unique_together for [section, slug, pub_date] on Article.
        db.create_unique('articles_article', ['section_id', 'slug', 'pub_date'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'TopicMetadata'
        db.delete_table('articles_topicmetadata')
        
        # Deleting model 'Article'
        db.delete_table('articles_article')
        
        # Deleting model 'Section'
        db.delete_table('articles_section')
        
        # Dropping ManyToManyField 'Article.authors'
        db.delete_table('articles_article_authors')
        
        # Deleting unique_together for [section, slug, pub_date] on Article.
        db.delete_unique('articles_article', ['section_id', 'slug', 'pub_date'])
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'articles.topicmetadata': {
            'description': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ForeignKey', ['Image'], {'null': 'True', 'blank': 'True'}),
            'link_name': ('models.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'link_url': ('models.URLField', [], {'null': 'True', 'blank': 'True'}),
            'topic': ('models.OneToOneField', ['Tag'], {'related_name': "'metadata'", 'unique': 'True'})
        },
        'articles.section': {
            'Meta': {'ordering': '["order",]'},
            'colour': ('models.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'menu_item': ('models.BooleanField', [], {'default': 'True'}),
            'order': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {}),
            'title': ('models.CharField', [], {'max_length': '100'})
        },
        'articles.article': {
            'Meta': {'ordering': "('-pub_date',)", 'unique_together': "(('section','slug','pub_date'),)", 'get_latest_by': "'pub_date'"},
            'approved': ('models.BooleanField', [], {'default': 'False'}),
            'authors': ('models.ManyToManyField', ['User'], {'blank': 'True'}),
            'body': ('models.TextField', [], {}),
            'featured': ('models.BooleanField', [], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ForeignKey', ['Image'], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('models.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'published': ('models.BooleanField', [], {'default': 'False'}),
            'score': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'section': ('models.ForeignKey', ['Section'], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {}),
            'summary': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('TagField', [], {}),
            'title': ('models.CharField', [], {'max_length': '100'})
        },
        'uploads.image': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'tagging.tag': {
            'Meta': {'ordering': "('name',)"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['articles']
