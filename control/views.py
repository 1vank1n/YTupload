# -*- coding: utf-8 -*-
import os, datetime
from django.conf import settings
from decorators import render_to
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from control.models import Log
from django.http import HttpResponse

@login_required
@render_to('index.html')
def index(request):
    if request.method == 'POST':
        filename = request.POST['filename']
        filesize = request.POST['filesize']
        title = request.POST['title']
        description = request.POST['description']
        keywords = request.POST['keywords']
        # проверить не конвертируется ли ещё?
        if Log.objects.filter(filename=filename):
            return HttpResponse('already in query')
        else:
            # записать в Log, поставить статус "конвертируется"
            l = Log(filename=filename, filesize=filesize, user=User.objects.filter(id=int(request.user.id))[0], created=datetime.datetime.now(), title=title, description=description, keywords=keywords, status='in query')
            l.save()
            return redirect('index')
    # действие по нажатию кнопки
    log_list = Log.objects.order_by('-id')[:10]
    # смотрим в директорию
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
        'loglist': log_list
    }
