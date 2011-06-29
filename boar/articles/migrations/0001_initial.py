# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Section'
        db.create_table('articles_section', (
            ('menu_item', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('colour', self.gf('django.db.models.fields.CharField')(max_length=7, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('tag_name', self.gf('django.db.models.fields.CharField')(default='Topics', max_length=100)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('articles', ['Section'])

        # Adding M2M table for field editors on 'Section'
        db.create_table('articles_section_editors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('section', models.ForeignKey(orm['articles.section'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('articles_section_editors', ['section_id', 'user_id'])

        # Adding model 'Position'
        db.create_table('articles_position', (
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('articles', ['Position'])

        # Adding M2M table for field members on 'Position'
        db.create_table('articles_position_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('position', models.ForeignKey(orm['articles.position'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('articles_position_members', ['position_id', 'user_id'])

        # Adding model 'Tag'
        db.create_table('articles_tag', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('articles', ['Tag'])

        # Adding model 'TaggedArticle'
        db.create_table('articles_taggedarticle', (
            ('content_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Article'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Tag'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('articles', ['TaggedArticle'])

        # Adding model 'Article'
        db.create_table('articles_article', (
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('tone', self.gf('django.db.models.fields.CharField')(default='article', max_length=25)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uploads.Image'], null=True, blank=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='articles', null=True, to=orm['archive.Page'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Section'])),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('articles', ['Article'])

        # Adding unique constraint on 'Article', fields ['section', 'slug', 'pub_date']
        db.create_unique('articles_article', ['section_id', 'slug', 'pub_date'])

        # Adding M2M table for field authors on 'Article'
        db.create_table('articles_article_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['articles.article'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('articles_article_authors', ['article_id', 'user_id'])

        # Adding model 'BookMetadata'
        db.create_table('articles_bookmetadata', (
            ('article', self.gf('django.db.models.fields.related.OneToOneField')(related_name='book_metadata', unique=True, to=orm['articles.Article'])),
            ('book_title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('articles', ['BookMetadata'])

        # Adding model 'LiveBlogMetadata'
        db.create_table('articles_liveblogmetadata', (
            ('twitter_username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('article', self.gf('django.db.models.fields.related.OneToOneField')(related_name='liveblog_metadata', unique=True, to=orm['articles.Article'])),
            ('since_tweet_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('articles', ['LiveBlogMetadata'])

        # Adding model 'GameMetadata'
        db.create_table('articles_gamemetadata', (
            ('article', self.gf('django.db.models.fields.related.OneToOneField')(related_name='game_metadata', unique=True, to=orm['articles.Article'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platform', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('articles', ['GameMetadata'])

        # Adding model 'MusicAlbumMetadata'
        db.create_table('articles_musicalbummetadata', (
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=37, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('article', self.gf('django.db.models.fields.related.OneToOneField')(related_name='musicalbum_metadata', unique=True, to=orm['articles.Article'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album_art', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('articles', ['MusicAlbumMetadata'])

        # Adding model 'MusicLiveMetadata'
        db.create_table('articles_musiclivemetadata', (
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('article', self.gf('django.db.models.fields.related.OneToOneField')(related_name='musiclive_metadata', unique=True, to=orm['articles.Article'])),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('articles', ['MusicLiveMetadata'])

        # Adding model 'PodcastMetadata'
        db.create_table('articles_podcastmetadata', (
            ('article', self.gf('django.db.models.fields.related.OneToOneField')(related_name='podcast_metadata', unique=True, to=orm['articles.Article'])),
            ('podcast', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('articles', ['PodcastMetadata'])

        # Adding model 'TravelMetadata'
        db.create_table('articles_travelmetadata', (
            ('article', self.gf('django.db.models.fields.related.OneToOneField')(related_name='travel_metadata', unique=True, to=orm['articles.Article'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('articles', ['TravelMetadata'])

        # Adding model 'Hit'
        db.create_table('articles_hit', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Article'])),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('articles', ['Hit'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Section'
        db.delete_table('articles_section')

        # Removing M2M table for field editors on 'Section'
        db.delete_table('articles_section_editors')

        # Deleting model 'Position'
        db.delete_table('articles_position')

        # Removing M2M table for field members on 'Position'
        db.delete_table('articles_position_members')

        # Deleting model 'Tag'
        db.delete_table('articles_tag')

        # Deleting model 'TaggedArticle'
        db.delete_table('articles_taggedarticle')

        # Deleting model 'Article'
        db.delete_table('articles_article')

        # Removing unique constraint on 'Article', fields ['section', 'slug', 'pub_date']
        db.delete_unique('articles_article', ['section_id', 'slug', 'pub_date'])

        # Removing M2M table for field authors on 'Article'
        db.delete_table('articles_article_authors')

        # Deleting model 'BookMetadata'
        db.delete_table('articles_bookmetadata')

        # Deleting model 'LiveBlogMetadata'
        db.delete_table('articles_liveblogmetadata')

        # Deleting model 'GameMetadata'
        db.delete_table('articles_gamemetadata')

        # Deleting model 'MusicAlbumMetadata'
        db.delete_table('articles_musicalbummetadata')

        # Deleting model 'MusicLiveMetadata'
        db.delete_table('articles_musiclivemetadata')

        # Deleting model 'PodcastMetadata'
        db.delete_table('articles_podcastmetadata')

        # Deleting model 'TravelMetadata'
        db.delete_table('articles_travelmetadata')

        # Deleting model 'Hit'
        db.delete_table('articles_hit')
    
    
    models = {
        'archive.issue': {
            'Meta': {'object_name': 'Issue'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'volume': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues'", 'to': "orm['archive.Volume']"})
        },
        'archive.page': {
            'Meta': {'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': "orm['archive.Part']"}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'archive.part': {
            'Meta': {'object_name': 'Part'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parts'", 'to': "orm['archive.Issue']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'archive.volume': {
            'Meta': {'object_name': 'Volume'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'articles.article': {
            'Meta': {'unique_together': "(('section', 'slug', 'pub_date'),)", 'object_name': 'Article'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uploads.Image']", 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'articles'", 'null': 'True', 'to': "orm['archive.Page']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tone': ('django.db.models.fields.CharField', [], {'default': "'article'", 'max_length': '25'})
        },
        'articles.bookmetadata': {
            'Meta': {'object_name': 'BookMetadata'},
            'article': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'book_metadata'", 'unique': 'True', 'to': "orm['articles.Article']"}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'book_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'articles.gamemetadata': {
            'Meta': {'object_name': 'GameMetadata'},
            'article': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'game_metadata'", 'unique': 'True', 'to': "orm['articles.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'articles.hit': {
            'Meta': {'object_name': 'Hit'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Article']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'articles.liveblogmetadata': {
            'Meta': {'object_name': 'LiveBlogMetadata'},
            'article': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'liveblog_metadata'", 'unique': 'True', 'to': "orm['articles.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'since_tweet_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'articles.musicalbummetadata': {
            'Meta': {'object_name': 'MusicAlbumMetadata'},
            'album_art': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'article': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'musicalbum_metadata'", 'unique': 'True', 'to': "orm['articles.Article']"}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '37', 'null': 'True', 'blank': 'True'})
        },
        'articles.musiclivemetadata': {
            'Meta': {'object_name': 'MusicLiveMetadata'},
            'article': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'musiclive_metadata'", 'unique': 'True', 'to': "orm['articles.Article']"}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'articles.podcastmetadata': {
            'Meta': {'object_name': 'PodcastMetadata'},
            'article': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'podcast_metadata'", 'unique': 'True', 'to': "orm['articles.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'podcast': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        'articles.position': {
            'Meta': {'object_name': 'Position'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'articles.section': {
            'Meta': {'object_name': 'Section'},
            'colour': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_item': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tag_name': ('django.db.models.fields.CharField', [], {'default': "'Topics'", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'articles.tag': {
            'Meta': {'object_name': 'Tag'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'articles.taggedarticle': {
            'Meta': {'object_name': 'TaggedArticle'},
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Tag']"})
        },
        'articles.travelmetadata': {
            'Meta': {'object_name': 'TravelMetadata'},
            'article': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'travel_metadata'", 'unique': 'True', 'to': "orm['articles.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'uploads.image': {
            'Meta': {'object_name': 'Image'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'images'", 'null': 'True', 'to': "orm['archive.Page']"}),
            'thumbnails': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['uploads.ThumbnailSize']", 'through': "orm['uploads.Thumbnail']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'upload': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'uploads.thumbnail': {
            'Meta': {'object_name': 'Thumbnail'},
            'bottom': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uploads.Image']"}),
            'left': ('django.db.models.fields.IntegerField', [], {}),
            'right': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uploads.ThumbnailSize']"}),
            'top': ('django.db.models.fields.IntegerField', [], {})
        },
        'uploads.thumbnailsize': {
            'Meta': {'object_name': 'ThumbnailSize'},
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }
    
    complete_apps = ['articles']
