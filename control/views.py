# -*- coding: utf-8 -*-
import os, datetime
from django.conf import settings
from decorators import render_to
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from control.forms import LogForm
from control.models import *

@login_required
@render_to('index.html')
def index(request):
    form = LogForm(request.POST or None)
    if form.is_valid():
        log = form.save(commit=False)
        log.user = request.user
        log.save()
        return redirect('index')    
    # обычная загрузка страницы
    ## simple load page
    log_list = Log.objects.order_by('-id')[:10]
    # смотрим в директорию
    # listing directory
    listdir = os.listdir(settings.ENCODE_DIR_FROM)
    logstatus_dict = dict(
        Log.objects.filter(
            filename__in=listdir
        ).values_list('filename', 'status')
    )
    file_list = [
        {'filename': file,
         'filesize': os.path.getsize(os.path.join(settings.ENCODE_DIR_FROM, file)),
         'status': logstatus_dict.get(file)
        } for file in listdir
    ]
    return {
        'dictdir': file_list,
        'loglist': log_list,
        'form': form
    }
