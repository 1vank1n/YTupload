# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from control.models import *

import os, datetime, settings

# функция вывода статуса
def LogStatus(l):
    try: return Log.objects.filter(filename=l)[0].status
    except: return None

def index(request, template):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/enter/')
    loglist = Log.objects.order_by('-id')[:10]
    # смотрим в директорию
    listdir = os.listdir(settings.ENCODE_DIR_FROM)
    dictdir = [{'filename':None,'filesize':None, 'status':None} for i in range(len(listdir))]
    n = 0
    for l in listdir:
        dictdir[n]['filename'] = l
        dictdir[n]['filesize'] = os.path.getsize(os.path.join(settings.ENCODE_DIR_FROM,l))
        dictdir[n]['status'] = LogStatus(l)
        n+=1
    # действие по нажатию кнопки
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
            return HttpResponseRedirect('/')
    return render_to_response(template, {'dictdir':dictdir,
                                         'loglist':loglist,})
                                         
def exit(request):
    logout(request)
    return HttpResponseRedirect('/enter/')

def enter(request, template):
    authform = AuthenticationForm()
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        authform = AuthenticationForm(data=request.POST)
        if authform.is_valid():
            login(request, authform.get_user())
            return HttpResponseRedirect('/')
    return render_to_response(template, {'authform': authform})
