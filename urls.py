from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^enter/$', 'django.contrib.auth.views.login', {'template_name': 'enter.html'}, name='login'),
    url(r'^exit/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    (r'^', include('control.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),                     
)
