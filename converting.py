# -*- coding: utf-8 -*-
import settings, os, datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from control.models import *

if Log.objects.filter(status='converting'):
    quit()
else:
    try:
        file = Log.objects.filter(status='in query')[0]
    except:
        quit()
    file.status = 'converting'
    file.save()
    # новое имя файла
    basename, extension = os.path.splitext(file.filename)
    newfilename = basename + '.flv'
    os.system('ffmpeg -i ' + os.path.join(settings.ENCODE_DIR_FROM, file.filename) + ' -ar 22050 -vb 1500kbits/s ' + os.path.join(settings.ENCODE_DIR_TO, newfilename))
    file.status = 'uploading'
    file.save()
    os.system('youtube-upload --email=' + settings.YT_LOGIN + ' --password=' + settings.YT_PASSWORD + ' --title="' + file.title.encode('utf-8') + '" --description="' + file.description.encode('utf-8') + '" --category="News" --keywords="' + file.keywords.encode('utf-8') + '" ' + os.path.join(settings.ENCODE_DIR_TO, newfilename).encode("utf-8"))
    file.status = 'uploaded'
    file.uploaded = datetime.datetime.now()
    file.save()