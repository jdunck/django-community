from django.db import models
from django.contrib.auth.models import User
from apps.community.managers import ActiveManager
import datetime

class EventType(models.Model):
    """
    Represents a type of event. We'll use this information to filter
    these events into their proper verticals.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __unicode__(self):
        return "%s" % (self.name,)

class Event(models.Model):
    """
    Stores the payload of data for the API.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    date = models.DateTimeField(default=datetime.datetime.now)
    creator = models.ForeignKey(User, null=True, blank=True)
    callback_url = models.URLField()
    source = models.CharField(max_length=255)
    source_url = models.URLField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(EventType)
    active = models.BooleanField(default=True)
    
    objects = ActiveManager()
    unfiltered = models.Manager()

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return "%s" % (self.name,)

    @models.permalink
    def get_absolute_url(self):
        # FIXME: Implement
        pass
