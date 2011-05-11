# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Volume'
        db.create_table('archive_volume', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('archive', ['Volume'])

        # Adding model 'Issue'
        db.create_table('archive_issue', (
            ('volume', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Volume'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('archive', ['Issue'])

        # Adding model 'Part'
        db.create_table('archive_part', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Issue'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['Part'])

        # Adding model 'Page'
        db.create_table('archive_page', (
            ('pdf', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Part'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('archive', ['Page'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Volume'
        db.delete_table('archive_volume')

        # Deleting model 'Issue'
        db.delete_table('archive_issue')

        # Deleting model 'Part'
        db.delete_table('archive_part')

        # Deleting model 'Page'
        db.delete_table('archive_page')
    
    
    models = {
        'archive.issue': {
            'Meta': {'object_name': 'Issue'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'volume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Volume']"})
        },
        'archive.page': {
            'Meta': {'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Part']"}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'archive.part': {
            'Meta': {'object_name': 'Part'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Issue']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'archive.volume': {
            'Meta': {'object_name': 'Volume'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['archive']
