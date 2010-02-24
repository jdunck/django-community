from apps.community.models import Event, EventType
from django.shortcuts import render_to_response

def index(request):
    events = Event.objects.all()
    articles = events.filter(category__name='articles')
    jobs = events.filter(category__name='jobs')
    pypi = events.filter(category__name='pypi')
    ext_dev = events.filter(category__name='ext_dev')
    return render_to_response('community/index.html',
                              {'article_list': articles,
                               'job_list': jobs,
                               'pypi_list': pypi,
                               'external_dev_list': ext_dev})

