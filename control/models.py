# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Log(models.Model):
    filename = models.CharField(max_length=300)
    filesize = models.CharField(max_length=300)
    user = models.ForeignKey(User)
    created = models.DateTimeField()
    uploaded = models.DateTimeField(null=True, blank=True)
    link = models.CharField(max_length=300, blank=True)
    playlist = models.CharField(max_length=300, blank=True)
    #youtube properties
    title = models.CharField(max_length=300)
    description = models.TextField()
    keywords = models.CharField(max_length=300)
    status = models.CharField(max_length=300, blank=True)
    
class People(models.Model):
    login = models.OneToOneField(User, primary_key=True)
    name = models.CharField(max_length=200)
    #playlist = models.CharField(max_length=300)