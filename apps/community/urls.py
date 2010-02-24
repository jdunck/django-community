from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'apps.community.views.index', name='community_home'),
)
