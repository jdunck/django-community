from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.comments.feeds import LatestCommentFeed
from django.contrib.comments.models import Comment
from django.contrib.sitemaps import views as sitemap_views
from django_website.apps.aggregator.feeds import CommunityAggregatorFeed
from django_website.apps.aggregator.models import FeedItem
from django_website.apps.blog.feeds import WeblogEntryFeed
from django_website.sitemaps import FlatPageSitemap, WeblogSitemap
from django.views.decorators.cache import cache_page

comments_info_dict = {
    'queryset': Comment.objects.filter(is_public=True).order_by('-submit_date'),
    'paginate_by': 15,
}

aggregator_info_dict = {
    'queryset': FeedItem.objects.select_related(),
    'paginate_by': 15,
}

feeds = {
    'weblog': WeblogEntryFeed,
    'comments': LatestCommentFeed,
    'community': CommunityAggregatorFeed,
}

sitemaps = {
    'weblog': WeblogSitemap,
    'flatpages': FlatPageSitemap,
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'homepage.html'}),
    (r'^accounts/', include('django_website.apps.accounts.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^comments/$', 'django.views.generic.list_detail.object_list', comments_info_dict),
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^community/add/(?P<feed_type_slug>[-\w]+)/',
         'django_website.apps.aggregator.views.add_feed',
          name='community-add-feed'),
    url(r'^community/add/',
         'django_website.apps.aggregator.views.feed_type_list',
          name="community-add-feed-list"),
    url(r'^community/(?P<feed_type_slug>[-\w]+)/',
         'django_website.apps.aggregator.views.feed_list',
          name="community-feed-list"),
    url(r'^community/', 'django_website.apps.aggregator.views.index', name='community-index'),
                       #    (r'^contact/', include('django_website.apps.contact.urls')),
                       #    (r'^documentation/', include('django_website.apps.docs.urls')),
    (r'^r/', include('django.conf.urls.shortcut')),
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^sitemap\.xml$', cache_page(sitemap_views.sitemap, 60 * 60 * 6), {'sitemaps': sitemaps}),
    (r'^weblog/', include('django_website.apps.blog.urls')),
    (r'^freenode\.9xJY7YIUWtwn\.html$', 'django.views.generic.simple.direct_to_template', {'template': 'freenode_tmp.html'}),
)

if settings.DEVELOPMENT_MODE:
    urlpatterns += patterns("django.views",
        url(r"^media/(?P<path>.*)", "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        }),
    )

urlpatterns += patterns('',
    # flatpages need to be last b/c they match anything
    (r'', include('django.contrib.flatpages.urls')),
)

admin.autodiscover()
