# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Log(models.Model):
    NONE, QUEUED, CONVERTING, UPLOADING, UPLOADED = range(1,6)
    STATUS_CHOICES = (
           ("1", "None"),
           ("2", "Queued"),
           ("3", "Converting"),
           ("4", "Uploading"),
           ("5", "Uploaded"),
    )
    filename = models.CharField('Файл', max_length=300)
    filesize = models.CharField('Размер', max_length=300)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(null=True, blank=True)
    link = models.CharField(max_length=300, blank=True)
    playlist = models.CharField(max_length=300, blank=True)
    #youtube properties
    title = models.CharField('Название', max_length=300)
    description = models.TextField('Описание')
    keywords = models.CharField('Ключевые слова', max_length=300)
    status = models.CharField(choices=STATUS_CHOICES, max_length=300, blank=True)
    
class People(models.Model):
    login = models.OneToOneField(User, primary_key=True)
    name = models.CharField(max_length=200)