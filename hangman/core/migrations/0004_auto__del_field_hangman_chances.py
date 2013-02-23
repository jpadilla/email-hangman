# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Hangman.chances'
        db.delete_column('core_hangman', 'chances')


    def backwards(self, orm):
        # Adding field 'Hangman.chances'
        db.add_column('core_hangman', 'chances',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    models = {
        'core.hangman': {
            'Meta': {'object_name': 'Hangman'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keys': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mistakes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'player': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'sender': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'used_letters': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']