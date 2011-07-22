# -*- coding: utf-8 -*-
import settings, os, datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from control.models import *

# если уже, что-то конвертится - выходим
# if something already converting - quit
if Log.objects.filter(status=Log.CONVERTING):
    quit()
else:
    # находим первый файл в очереди
    # find first file in queue
    log_list = Log.objects.filter(status=Log.QUEUED)
    if not log_list:
        quit()
    # меняем статус на "конвертируется"
    # change status to "converting"  
    file = log_list[0]
    file.status = Log.CONVERTING
    file.save()
    # переназываем файл
    # rename file
    basename, extension = os.path.splitext(file.filename)
    newfilename = basename + '.flv'
    # запускаем конвертирование
    # start converting
    os.system('ffmpeg -i ' + os.path.join(settings.ENCODE_DIR_FROM, file.filename) + \
              ' -ar 22050 -vb 1500kbits/s ' + os.path.join(settings.ENCODE_DIR_TO, newfilename))
    file.status = Log.UPLOADING
    file.save()
    # загружаем на youtube
    # start uploading to youtube
    os.system('youtube-upload --email=' + settings.YT_LOGIN + \ 
              ' --password=' + settings.YT_PASSWORD + \
              ' --title="' + file.title.encode('utf-8') + \
              '" --description="' + file.description.encode('utf-8') + \
              '" --category="News" --keywords="' + file.keywords.encode('utf-8') + \
              '" ' + os.path.join(settings.ENCODE_DIR_TO, newfilename).encode("utf-8"))
    file.status = Log.UPLOADED
    file.uploaded = datetime.datetime.now()
    file.save()