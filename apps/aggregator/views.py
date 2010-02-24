from django.shortcuts import render_to_response
from apps.aggregator.models import FeedItem, Feed, FeedType

def community_index(request):
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
