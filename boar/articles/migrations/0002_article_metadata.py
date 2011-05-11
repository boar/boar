
from south.db import db
from django.db import models
from boar.articles.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'BookMetadata'
        db.create_table('articles_bookmetadata', (
            ('article', models.OneToOneField(orm.Article, related_name='book_metadata', unique=True)),
            ('publisher', models.CharField(max_length=100, null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('author', models.CharField(max_length=100)),
        ))
        db.send_create_signal('articles', ['BookMetadata'])
        
        # Adding model 'GamesMetadata'
        db.create_table('articles_gamesmetadata', (
            ('article', models.OneToOneField(orm.Article, related_name='games_metadata', unique=True)),
            ('score', models.IntegerField(null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('platform', models.CharField(max_length=50)),
        ))
        db.send_create_signal('articles', ['GamesMetadata'])
        
        # Adding model 'MusicLiveMetadata'
        db.create_table('articles_musiclivemetadata', (
            ('artist', models.CharField(max_length=100)),
            ('score', models.IntegerField(null=True, blank=True)),
            ('location', models.CharField(max_length=100, null=True, blank=True)),
            ('date', models.DateField(null=True, blank=True)),
            ('article', models.OneToOneField(orm.Article, related_name='musiclive_metadata', unique=True)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('articles', ['MusicLiveMetadata'])
        
        # Adding model 'MusicAlbumMetadata'
        db.create_table('articles_musicalbummetadata', (
            ('artist', models.CharField(max_length=100)),
            ('label', models.CharField(max_length=100, null=True, blank=True)),
            ('mbid', models.CharField(max_length=37, null=True, blank=True)),
            ('score', models.IntegerField(null=True, blank=True)),
            ('article', models.OneToOneField(orm.Article, related_name='musicalbum_metadata', unique=True)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('articles', ['MusicAlbumMetadata'])
        
        # Deleting field 'TopicMetadata.link_url'
        db.delete_column('articles_topicmetadata', 'link_url')
        
        # Deleting field 'TopicMetadata.link_name'
        db.delete_column('articles_topicmetadata', 'link_name')
        
        # Deleting field 'Article.score'
        db.delete_column('articles_article', 'score')
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'BookMetadata'
        db.delete_table('articles_bookmetadata')
        
        # Deleting model 'GamesMetadata'
        db.delete_table('articles_gamesmetadata')
        
        # Deleting model 'MusicLiveMetadata'
        db.delete_table('articles_musiclivemetadata')
        
        # Deleting model 'MusicAlbumMetadata'
        db.delete_table('articles_musicalbummetadata')
        
        # Adding field 'TopicMetadata.link_url'
        db.add_column('articles_topicmetadata', 'link_url', models.URLField(null=True, blank=True))
        
        # Adding field 'TopicMetadata.link_name'
        db.add_column('articles_topicmetadata', 'link_name', models.CharField(max_length=100, null=True, blank=True))
        
        # Adding field 'Article.score'
        db.add_column('articles_article', 'score', models.IntegerField(null=True, blank=True))
        
    
    
    models = {
        'articles.bookmetadata': {
            'article': ('models.OneToOneField', ['Article'], {'related_name': "'book_metadata'", 'unique': 'True'}),
            'author': ('models.CharField', [], {'max_length': '100'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('models.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'articles.musiclivemetadata': {
            'article': ('models.OneToOneField', ['Article'], {'related_name': "'musiclive_metadata'", 'unique': 'True'}),
            'artist': ('models.CharField', [], {'max_length': '100'}),
            'date': ('models.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'location': ('models.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'score': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'articles.topicmetadata': {
            'description': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ForeignKey', ['Image'], {'null': 'True', 'blank': 'True'}),
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
            'section': ('models.ForeignKey', ['Section'], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {}),
            'summary': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('TagField', [], {}),
            'title': ('models.CharField', [], {'max_length': '100'})
        },
        'articles.musicalbummetadata': {
            'article': ('models.OneToOneField', ['Article'], {'related_name': "'musicalbum_metadata'", 'unique': 'True'}),
            'artist': ('models.CharField', [], {'max_length': '100'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'label': ('models.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mbid': ('models.CharField', [], {'max_length': '37', 'null': 'True', 'blank': 'True'}),
            'score': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'uploads.image': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'articles.gamesmetadata': {
            'article': ('models.OneToOneField', ['Article'], {'related_name': "'games_metadata'", 'unique': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'platform': ('models.CharField', [], {'max_length': '50'}),
            'score': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'tagging.tag': {
            'Meta': {'ordering': "('name',)"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['articles']
