
from south.db import db
from django.db import models
from boar.uploads.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ThumbnailSize'
        db.create_table('uploads_thumbnailsize', (
            ('width', models.IntegerField()),
            ('height', models.IntegerField()),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=100)),
        ))
        db.send_create_signal('uploads', ['ThumbnailSize'])
        
        # Adding model 'Audio'
        db.create_table('uploads_audio', (
            ('upload_date', models.DateTimeField()),
            ('author', models.ForeignKey(orm['auth.User'], null=True, blank=True)),
            ('upload', models.FileField(upload_to=settings.UPLOAD_DIRECTORY)),
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(max_length=100)),
        ))
        db.send_create_signal('uploads', ['Audio'])
        
        # Adding model 'Image'
        db.create_table('uploads_image', (
            ('upload_date', models.DateTimeField()),
            ('author', models.ForeignKey(orm['auth.User'], null=True, blank=True)),
            ('upload', models.ImageField(upload_to=settings.UPLOAD_DIRECTORY)),
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(max_length=100)),
        ))
        db.send_create_signal('uploads', ['Image'])
        
        # Adding model 'Thumbnail'
        db.create_table('uploads_thumbnail', (
            ('right', models.IntegerField()),
            ('bottom', models.IntegerField()),
            ('top', models.IntegerField()),
            ('id', models.AutoField(primary_key=True)),
            ('size', models.ForeignKey(orm.ThumbnailSize)),
            ('image', models.ForeignKey(orm.Image)),
            ('left', models.IntegerField()),
        ))
        db.send_create_signal('uploads', ['Thumbnail'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ThumbnailSize'
        db.delete_table('uploads_thumbnailsize')
        
        # Deleting model 'Audio'
        db.delete_table('uploads_audio')
        
        # Deleting model 'Image'
        db.delete_table('uploads_image')
        
        # Deleting model 'Thumbnail'
        db.delete_table('uploads_thumbnail')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'uploads.thumbnailsize': {
            'height': ('models.IntegerField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '100'}),
            'width': ('models.IntegerField', [], {})
        },
        'uploads.audio': {
            'author': ('models.ForeignKey', ['User'], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'title': ('models.CharField', [], {'max_length': '100'}),
            'upload': ('models.FileField', [], {'upload_to': 'settings.UPLOAD_DIRECTORY'}),
            'upload_date': ('models.DateTimeField', [], {})
        },
        'uploads.image': {
            'author': ('models.ForeignKey', ['User'], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'thumbnails': ('models.ManyToManyField', ['ThumbnailSize'], {'through': "'Thumbnail'"}),
            'title': ('models.CharField', [], {'max_length': '100'}),
            'upload': ('models.ImageField', [], {'upload_to': 'settings.UPLOAD_DIRECTORY'}),
            'upload_date': ('models.DateTimeField', [], {})
        },
        'uploads.thumbnail': {
            'bottom': ('models.IntegerField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ForeignKey', ['Image'], {}),
            'left': ('models.IntegerField', [], {}),
            'right': ('models.IntegerField', [], {}),
            'size': ('models.ForeignKey', ['ThumbnailSize'], {}),
            'top': ('models.IntegerField', [], {})
        }
    }
    
    complete_apps = ['uploads']
