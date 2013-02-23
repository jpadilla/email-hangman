# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hangman'
        db.create_table('core_hangman', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('player', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('used_letters', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mistakes', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('core', ['Hangman'])


    def backwards(self, orm):
        # Deleting model 'Hangman'
        db.delete_table('core_hangman')


    models = {
        'core.hangman': {
            'Meta': {'object_name': 'Hangman'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mistakes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'player': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'sender': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'used_letters': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']