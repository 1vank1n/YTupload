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
    os.system('nice -n 20 ffmpeg -i ' + os.path.join(settings.ENCODE_DIR_FROM, file.filename) + \
              ' -ar ' + settings.FFMPEG_AR + \
              ' -vb ' + settings.FFMPEG_VB + \
              ' ' + os.path.join(settings.ENCODE_DIR_TO, newfilename))
    file.status = Log.UPLOADING
    file.save()
    
    # загружаем на youtube
    # start uploading to youtube
    import gdata.youtube
    import gdata.youtube.service

    yt_service = gdata.youtube.service.YouTubeService()
    # A complete client login request
    yt_service.email = settings.YT_LOGIN
    yt_service.password = settings.YT_PASSWORD
    yt_service.developer_key = settings.YT_DEVKEY
    yt_service.ProgrammaticLogin()

    # prepare a media group object to hold our video's meta-data
    my_media_group = gdata.media.Group(
    title=gdata.media.Title(text=file.title.encode('utf-8')),
    description=gdata.media.Description(description_type='plain', text=file.description.encode('utf-8')),
    keywords=gdata.media.Keywords(text=file.keywords.encode('utf-8')),
    category=[gdata.media.Category(
                text='News',
                scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                label='News')],
    player=None
    )
    
    # create the gdata.youtube.YouTubeVideoEntry to be uploaded
    video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)

    # set the path for the video file binary
    video_file_location = os.path.join(settings.ENCODE_DIR_TO, newfilename).encode("utf-8")
    new_entry = yt_service.InsertVideoEntry(video_entry, video_file_location)
    
    # completed upload, check link
    file.link = new_entry.media.player.url
    file.status = Log.UPLOADED
    file.uploaded = datetime.datetime.now()
    file.save()
