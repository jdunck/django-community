from django.core.exceptions import ValidationError
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc
from apps.community.models import Event, EventType

class AnonymousEventHandler(AnonymousBaseHandler):
    model = Event

    def read(self, request, *args, **kwargs):
        return self.model.objects.filter(category__slug=kwargs['event_type'])


class EventHandler(BaseHandler):
    alowed_methods = ('GET', 'POST')
    model = Event
    anonymous = AnonymousEventHandler
    
    # TODO: See if removing this still works.
    def read(self, request, *args, **kwargs):
        return self.model.objects.filter(category__slug=kwargs['event_type'])

    def create(self, request, event_type):
        """
        Mostly pulled from the piston basic handler, but we need to
        link the EventType model when saving a new instance.
        """
        attrs = self.flatten_dict(request.POST)
        if not attrs:
            return rc.BAD_REQUEST

        if request.user.is_authenticated():
            attrs['creator'] = request.user
        try:
            et = EventType.objects.get(slug=event_type)
            attrs['category'] = et
        except EventType.DoesNotExist:
            return rc.BAD_REQUEST
        except KeyError:
            return rc.BAD_REQUEST

        try:
            inst = self.model.objects.get(**attrs)
            return rc.DUPLICATE_ENTRY
        except (self.model.DoesNotExist, ValidationError):
            # some things, such as date, are nullable, but are added
            # during creation
            inst = self.model.objects.create(**attrs)
            inst.save()
            return rc.CREATED
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY
