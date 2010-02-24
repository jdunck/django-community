from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from apps.community.handlers import EventHandler

auth = HttpBasicAuthentication(realm='Django Community API')
event_handler = Resource(EventHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^(?P<event_type>[-\w]+)/', event_handler, name="api-endpoint"),
)
