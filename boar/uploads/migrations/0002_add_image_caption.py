
from south.db import db
from django.db import models
from boar.uploads.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Image.caption'
        db.add_column('uploads_image', 'caption', models.CharField(max_length=255, null=True, blank=True))
    
    
    def backwards(self, orm):
        
        # Deleting field 'Image.caption'
        db.delete_column('uploads_image', 'caption')
    
    
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
            'author': ('models.ForeignKey', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'title': ('models.CharField', [], {'max_length': '100'}),
            'upload': ('models.FileField', [], {}),
            'upload_date': ('models.DateTimeField', [], {})
        },
        'uploads.image': {
            'author': ('models.ForeignKey', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'}),
            'caption': ('models.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'thumbnails': ('models.ManyToManyField', ["orm['uploads.ThumbnailSize']"], {'through': "'Thumbnail'"}),
            'title': ('models.CharField', [], {'max_length': '100'}),
            'upload': ('models.ImageField', [], {}),
            'upload_date': ('models.DateTimeField', [], {})
        },
        'uploads.thumbnail': {
            'bottom': ('models.IntegerField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ForeignKey', ["orm['uploads.Image']"], {}),
            'left': ('models.IntegerField', [], {}),
            'right': ('models.IntegerField', [], {}),
            'size': ('models.ForeignKey', ["orm['uploads.ThumbnailSize']"], {}),
            'top': ('models.IntegerField', [], {})
        }
    }
    
    complete_apps = ['uploads']
