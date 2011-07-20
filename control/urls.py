from django.conf.urls.defaults import *

urlpatterns = patterns('control.views',
    url(r'^$', 'index', name='index'),
)
