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
    if log_list:
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
        file.status = Log.READYUPLOAD
        file.save()
    
if Log.objects.filter(status=Log.UPLOADING):
    quit()
else:
    # находим первый файл в очереди на загрузку
    # find first file in queue to upload
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
        video_file_location = os.path.join(settings.ENCODE_DIR_TO, newfilename).encode("utf-8")
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