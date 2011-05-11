
from south.db import db
from django.db import models
from boar.articles.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'Article.approved'
        db.alter_column('articles_article', 'approved', models.BooleanField(default=True, editable=False))
        
    
    
    def backwards(self, orm):
        
        # Changing field 'Article.approved'
        db.alter_column('articles_article', 'approved', models.BooleanField(default=False))
        
    
    
    models = {
        'articles.bookmetadata': {
            'article': ('models.OneToOneField', ["orm['articles.Article']"], {'related_name': "'book_metadata'", 'unique': 'True'}),
            'author': ('models.CharField', [], {'max_length': '100'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('models.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'articles.musiclivemetadata': {
            'article': ('models.OneToOneField', ["orm['articles.Article']"], {'related_name': "'musiclive_metadata'", 'unique': 'True'}),
            'artist': ('models.CharField', [], {'max_length': '100'}),
            'date': ('models.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'location': ('models.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'tagging.tag': {
            'Meta': {'ordering': "('name',)"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'articles.topicmetadata': {
            'description': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ForeignKey', ["orm['uploads.Image']"], {'null': 'True', 'blank': 'True'}),
            'topic': ('models.OneToOneField', ["orm['tagging.Tag']"], {'related_name': "'metadata'", 'unique': 'True'})
        },
        'articles.section': {
            'Meta': {'ordering': "['order',]"},
            'colour': ('models.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'editors': ('models.ManyToManyField', ["orm['auth.User']"], {'blank': 'True'}),
            'email': ('models.EmailField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'menu_item': ('models.BooleanField', [], {'default': 'True'}),
            'order': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {}),
            'tag_name': ('models.CharField', [], {'default': "'Topics'", 'max_length': '100'}),
            'title': ('models.CharField', [], {'max_length': '100'})
        },
        'articles.position': {
            'Meta': {'ordering': "['order',]"},
            'email': ('models.EmailField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'members': ('models.ManyToManyField', ["orm['auth.User']"], {'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '100'}),
            'order': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {})
        },
        'articles.musicalbummetadata': {
            'album_art': ('models.ImageField', [], {'null': 'True', 'blank': 'True'}),
            'article': ('models.OneToOneField', ["orm['articles.Article']"], {'related_name': "'musicalbum_metadata'", 'unique': 'True'}),
            'artist': ('models.CharField', [], {'max_length': '100'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'label': ('models.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'link': ('models.URLField', [], {'null': 'True', 'blank': 'True'}),
            'mbid': ('models.CharField', [], {'max_length': '37', 'null': 'True', 'blank': 'True'})
        },
        'uploads.image': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'articles.gamesmetadata': {
            'article': ('models.OneToOneField', ["orm['articles.Article']"], {'related_name': "'games_metadata'", 'unique': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'platform': ('models.CharField', [], {'max_length': '50'})
        },
        'articles.hit': {
            'article': ('models.ForeignKey', ["orm['articles.Article']"], {}),
            'date': ('models.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('models.IPAddressField', [], {}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'})
        },
        'articles.article': {
            'Meta': {'ordering': "('-pub_date',)", 'unique_together': "(('section','slug','pub_date'),)", 'get_latest_by': "'pub_date'"},
            'approved': ('models.BooleanField', [], {'default': 'True', 'editable': 'False'}),
            'authors': ('models.ManyToManyField', ["orm['auth.User']"], {'blank': 'True'}),
            'body': ('models.TextField', [], {}),
            'featured': ('models.BooleanField', [], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ForeignKey', ["orm['uploads.Image']"], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('models.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'published': ('models.BooleanField', [], {'default': 'False'}),
            'score': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'section': ('models.ForeignKey', ["orm['articles.Section']"], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {}),
            'summary': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('TagField', [], {}),
            'title': ('models.CharField', [], {'max_length': '100'}),
            'tone': ('models.CharField', [], {'default': "'article'", 'max_length': '25'})
        }
    }
    
    complete_apps = ['articles']
