# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from control.models import *

class LogAdmin(admin.ModelAdmin):
    list_display = ('title','keywords','status','filename','filesize','user','created','uploaded','link','playlist',)
admin.site.register(Log, LogAdmin)

class PeopleAdmin(admin.ModelAdmin):
    list_display = ('login', 'name', )
admin.site.register(People, PeopleAdmin)