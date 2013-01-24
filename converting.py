# -*- coding: utf-8 -*-
import os, datetime, subprocess
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
from control.models import *

# если уже, что-то конвертится - выходим
# if something already converting - quit
if Log.objects.filter(status=Log.CONVERTING):
    quit()
else:
    # находим первый файл в очереди
    # find first file in queue
    log_list = Log.objects.filter(status=Log.QUEUED)
    if log_list:
        # меняем статус на "конвертируется"
        # change status to "converting"  
        file = log_list[0]
        file.status = Log.CONVERTING
        file.save()
        
        if file.convert:
            # переназываем файл
            # rename file
            basename, extension = os.path.splitext(file.filename)
            newfilename = basename + '.flv'
            audiofilename = os.path.join(settings.ENCODE_DIR_TO, 'audio.wav')
            # запускаем конвертирование
            # start converting
            # 1. split audio
            subprocess.call(['nice', '-n', '20', 'ffmpeg', '-y', '-i', os.path.join(settings.ENCODE_DIR_FROM, file.filename), '-acodec', 'pcm_s16le', audiofilename])
            # 2. normalize audio
            subprocess.call(['normalize-audio', audiofilename])
            # 3. merge video and audio
            subprocess.call(['nice', '-n', '20', 'ffmpeg', '-y', '-i', 
                             os.path.join(settings.ENCODE_DIR_FROM, file.filename),
                             '-i', audiofilename, '-map', '0:0', '-map', '1:0',
                             '-ar', settings.FFMPEG_AR, '-vb', settings.FFMPEG_VB,
                             os.path.join(settings.ENCODE_DIR_TO, newfilename) ])

            file.status = Log.READYUPLOAD
            file.save()
        else:
            file.status = Log.READYUPLOAD
            file.save()
                
    
if Log.objects.filter(status=Log.UPLOADING):
    quit()
else:
    # находим первый файл в очереди на загрузку
    # find first file in queue to upload
    print '#### start uploading ####'
    log_list = Log.objects.filter(status=Log.READYUPLOAD)
    if log_list:
        file = log_list[0]
        file.status = Log.UPLOADING
        file.save()
        
        # переназываем файл
        # rename file
        basename, extension = os.path.splitext(file.filename)
        newfilename = basename + '.flv'
            
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
        
        if file.convert:
            video_file_location = os.path.join(settings.ENCODE_DIR_TO, newfilename).encode("utf-8")
        else:
            video_file_location = os.path.join(settings.ENCODE_DIR_FROM, file.filename).encode("utf-8")
        new_entry = yt_service.InsertVideoEntry(video_entry, video_file_location)
        
        # add to playlist
        if file.playlist:
            playlist_uri = 'http://gdata.youtube.com/feeds/api/playlists/%s' % file.playlist
            video_id = new_entry.id.text[-11:]
            playlist_video_entry = yt_service.AddPlaylistVideoEntryToPlaylist(playlist_uri, video_id) 
        
        # completed upload, check link
        file.link = new_entry.media.player.url
        file.status = Log.UPLOADED
        file.uploaded = datetime.datetime.now()
        file.save()
