
from south.db import db
from django.db import models
from boar.articles.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'MusicAlbumMetadata.link'
        db.add_column('articles_musicalbummetadata', 'link', models.URLField(null=True, blank=True))
        
        # Adding field 'MusicAlbumMetadata.album_art'
        db.add_column('articles_musicalbummetadata', 'album_art', models.ImageField(null=True, blank=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'MusicAlbumMetadata.link'
        db.delete_column('articles_musicalbummetadata', 'link')
        
        # Deleting field 'MusicAlbumMetadata.album_art'
        db.delete_column('articles_musicalbummetadata', 'album_art')
        
    
    
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
            'location': ('models.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
            'pub_date': ('models.DateTimeField', [], {'default': 'datetime.datetime(2009, 5, 9, 20, 42, 34, 136460)'}),
            'published': ('models.BooleanField', [], {'default': 'False'}),
            'score': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'section': ('models.ForeignKey', ['Section'], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {}),
            'summary': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('TagField', [], {}),
            'title': ('models.CharField', [], {'max_length': '100'}),
            'tone': ('models.CharField', [], {'default': "'article'", 'max_length': '25'})
        },
        'articles.musicalbummetadata': {
            'album_art': ('models.ImageField', [], {}),
            'article': ('models.OneToOneField', ['Article'], {'related_name': "'musicalbum_metadata'", 'unique': 'True'}),
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
            'article': ('models.OneToOneField', ['Article'], {'related_name': "'games_metadata'", 'unique': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'platform': ('models.CharField', [], {'max_length': '50'})
        },
        'tagging.tag': {
            'Meta': {'ordering': "('name',)"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['articles']
