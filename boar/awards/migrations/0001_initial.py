# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Ceremony'
        db.create_table('awards_ceremony', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('awards', ['Ceremony'])

        # Adding model 'Award'
        db.create_table('awards_award', (
            ('ceremony', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['awards.Ceremony'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('awards', ['Award'])

        # Adding model 'Nominee'
        db.create_table('awards_nominee', (
            ('order', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('award', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['awards.Award'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('awards', ['Nominee'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Ceremony'
        db.delete_table('awards_ceremony')

        # Deleting model 'Award'
        db.delete_table('awards_award')

        # Deleting model 'Nominee'
        db.delete_table('awards_nominee')
    
    
    models = {
        'awards.award': {
            'Meta': {'object_name': 'Award'},
            'ceremony': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['awards.Ceremony']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'awards.ceremony': {
            'Meta': {'object_name': 'Ceremony'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'awards.nominee': {
            'Meta': {'object_name': 'Nominee'},
            'award': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['awards.Award']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['awards']
