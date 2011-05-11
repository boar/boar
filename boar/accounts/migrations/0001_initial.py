
from south.db import db
from django.db import models
from boar.accounts.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('accounts_userprofile', (
            ('about', models.TextField(null=True, blank=True)),
            ('photo', models.ImageField(null=True, upload_to='images/user/', blank=True)),
            ('articles_graph', models.ImageField(null=True, upload_to='graphs/user_articles/', blank=True)),
            ('user', models.ForeignKey(orm['auth.User'], unique=True)),
            ('position', models.CharField(max_length=100, null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('accounts', ['UserProfile'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('accounts_userprofile')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'accounts.userprofile': {
            'about': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'articles_graph': ('models.ImageField', [], {'null': 'True', 'upload_to': "'graphs/user_articles/'", 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'photo': ('models.ImageField', [], {'null': 'True', 'upload_to': "'images/user/'", 'blank': 'True'}),
            'position': ('models.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('models.ForeignKey', ['User'], {'unique': 'True'})
        }
    }
    
    complete_apps = ['accounts']
