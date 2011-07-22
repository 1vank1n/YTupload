# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django import forms
from models import Log

class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ['filename', 'title', 'description', 'keywords']

    def clean_filename(self):
        filename = self.cleaned_data.get('filename')
        if Log.objects.filter(filename=filename):
            raise forms.ValidationError('already in query')
        return filename

    def save(self, commit=True):
        log = super(LogForm, self).save(commit)
        log.filesize = os.path.getsize(os.path.join(settings.ENCODE_DIR_FROM, log.filename))
        log.status = Log.QUEUED
        if commit:
            log.save()
        return log