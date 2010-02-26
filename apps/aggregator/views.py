from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
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

@login_required
def add_feed(request, feed_type_slug):
    import pdb; pdb.set_trace() # FIXME
    initial_data = {'feed_type': FeedType.objects.get(slug=feed_type_slug)}
    f = FeedModelForm(request.POST or None, initial=initial_data)
    if f.is_valid():
        # success
        pass
    else:
        return render_to_response('community/add_feed.html',
                                  {'form':f})
