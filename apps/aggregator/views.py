from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list
from apps.aggregator.models import FeedItem, Feed, FeedType
from apps.aggregator.forms import FeedModelForm

def index(request):
    item_list = FeedItem.objects.all()
    articles = item_list.filter(feed__feed_type__slug='articles')
    jobs = item_list.filter(feed__feed_type__slug='jobs')
    pypi = item_list.filter(feed__feed_type__slug='pypi')
    external_dev = item_list.filter(feed__feed_type__slug='external-dev')
    twitter = item_list.filter(feed__feed_type__slug='twitter')

    return render_to_response('aggregator/index.html',
                              {'article_list': articles,
                               'job_list':jobs,
                               'pypi_list':pypi,
                               'external_dev_list': external_dev,
                               'twitter_list': twitter,
                              })

def feed_list(request, feed_type_slug):
    feed_type = get_object_or_404(FeedType, slug=feed_type_slug)
    items = FeedItem.objects.filter(feed__feed_type=feed_type)
    return object_list(request, items)

def feed_type_list(request):
    return object_list(request, FeedType.objects.all())

@login_required
def add_feed(request, feed_type_slug):
    initial_data = {'feed_type': FeedType.objects.get(slug=feed_type_slug).id}
    f = FeedModelForm(request.POST or None, initial=initial_data)
    if f.is_valid():
        if f.save():
            return HttpResponseRedirect(reverse('community-index'))
        else:
            # not sure when this happens.
            return render_to_response('aggregator/add_feed.html',
                                      {'form':f})
    else:
        return render_to_response('aggregator/add_feed.html',
                                  {'form':f})
