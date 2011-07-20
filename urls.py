from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
import views, settings

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', views.index, {'template': 'index.html'}),
    (r'^enter/$', views.enter, {'template': 'enter.html'}),
    (r'^exit/$', views.exit),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),                     
)
