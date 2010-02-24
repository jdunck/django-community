import unittest
import httplib as httplib
import base64
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        from django.utils import simplejson as json
from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from piston.utils import rc

from apps.community.models import EventType, Event
from apps.community.handlers import EventHandler

class CommunityAPITests(unittest.TestCase):
    def setUp(self):
        class FakeUser:
            is_authenticated = lambda x: False
        class FakeRequestObject:
            POST = {
                'name':'test1',
                'slug':'test1',
                'date':'2010-01-01 12:30',
                'callback_url':'http://djangoproject.com/community/',
                'source':'Django Project',
                'source_url':'http://djangoproject.com/',
                }
            user = FakeUser()
        self.event_type = event_type_gen(name='test')
        self.event = event_gen(name='test event')
        self.api_view = EventHandler()
        self.fake_req_obj = FakeRequestObject()

    def test_api_creation(self):
        try:
            self.api_view.create(self.fake_req_obj, 'test')
        except Exception, e:
            # should never hit this.
            assert(False)

    def test_duplicate_entry_creation(self):
        self.api_view.create(self.fake_req_obj, 'test') # tested by test_api_creation method
        self.assertEqual(self.api_view.create(self.fake_req_obj, 'test').content, 'Conflict/Duplicate')

    def tearDown(self):
        Event.objects.all().delete()
        EventType.objects.all().delete()

class APIIntegrationTests(TestCase):
    def setUp(self):
        PASSWORD = 'passw0rd'
        self.user = User(username='arthur', email='king@britons.gov.uk',)
        self.user.set_password(PASSWORD)
        self.user.save()
        
        self.bad_user = User(username='robin', email='brave@britons.gov.uk',)
        self.bad_user.set_password(PASSWORD)
        self.bad_user.save()
         
        self.auth_string = 'Basic %s' % base64.encodestring('%s:%s' % (self.user.username, PASSWORD))
        self.bad_user_auth_string = 'Basic %s' % base64.encodestring('%s:%s' % (self.bad_user.username, PASSWORD))

        self.event = event_gen(category=event_type_gen(name='test'))

    def testGET(self):
        url = reverse('api-endpoint', args=['test'])
        
        req = self.client.get(url)
        self.assertTrue(req.status_code == httplib.OK)
        
        req = self.client.get(url, HTTP_AUTHORIZATION=self.bad_user_auth_string)
        self.assertTrue(req.status_code == httplib.OK)
        
        req = self.client.get(url + '?format=json', HTTP_AUTHORIZATION=self.auth_string)
        self.assertTrue(req.status_code == httplib.OK)
        event = json.loads(req.content)
        self.assertTrue(event[0]['name'] == Event.objects.get(slug=self.event.slug).name)

    def testPOST(self):
        tempevent= {
            'name':'Enchanter',
            'slug':'enchanter',
            'date':'2010-01-01 12:30',
            'callback_url':'http://djangoproject.com/community/',
            'source':'Django Project',
            'source_url':'http://djangoproject.com/',
            'description':'Summon up fire without flint or tinder',
            }

        url = reverse('api-endpoint', args=['test'])
        
        req = self.client.post(url, tempevent)
        self.assertTrue(req.status_code == httplib.UNAUTHORIZED)
        
        req = self.client.post(url, { }, HTTP_AUTHORIZATION=self.auth_string)
        self.assertTrue(req.status_code == httplib.BAD_REQUEST)
        
        req = self.client.post(url, tempevent, HTTP_AUTHORIZATION=self.auth_string)
        self.assertTrue(req.status_code == httplib.CREATED)
        self.assertTrue(Event.objects.filter(name=tempevent['name']).count() == 1)
   
    def tearDown(self):
        Event.objects.all().delete()
        EventType.objects.all().delete()
        User.objects.all().delete()


def event_type_gen(**kwargs):
    kwargs.setdefault('name', 'Test Event Type')
    kwargs.setdefault('slug', slugify(kwargs['name']))
    return EventType.objects.create(**kwargs)

def event_gen(**kwargs):
    if not EventType.objects.count():
        event_type_gen()
    kwargs.setdefault('name', 'Holy Grail Seeker')
    kwargs.setdefault('slug', slugify(kwargs['name']))
    kwargs.setdefault('date', datetime.now())
    kwargs.setdefault('callback_url', 'http://google.com/search?q=grail')
    kwargs.setdefault('source', 'Kingdom of Camelot')
    kwargs.setdefault('source_url', 'http://camelot.com/')
    kwargs.setdefault('description', 'It is your sacred task to seek this Grail.')
    kwargs.setdefault('category', EventType.objects.all().order_by('?')[0])
    return Event.objects.create(**kwargs)
    
