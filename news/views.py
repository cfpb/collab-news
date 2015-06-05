from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import cache_page
from django.template import RequestContext
from django.conf import settings

from models import NewsItem, NewsFeed

TEMPLATE_PATH = 'news/'


def _create_params(req):
    p = {'is_news': True, }
    if settings.WIKI_INSTALLED:
        p['wiki_installed'] = True
        p['wiki_search_autocomplete_json_url'] = \
            settings.WIKI_SEARCH_URL % ('5', '')
    p.update(csrf(req))
    return p


@login_required
@cache_page(60 * 5)
def news_item(req, slug):
    p = _create_params(req)
    p['item'] = get_object_or_404(NewsItem, slug=slug, published=True)
    return render_to_response(TEMPLATE_PATH + "article.html", p,
                              context_instance=RequestContext(req))


@login_required
@cache_page(60 * 5)
def news_list(req, slug=None):
    p = _create_params(req)
    news = NewsItem.objects.filter(published=True). \
        order_by('-publish_date')
    if slug:
        feed = get_object_or_404(NewsFeed, slug=slug)
        p['selected_feed'] = feed
        news = news.filter(feed_id=feed.id)
    p['sticky_items'] = news.filter(sticky=True)
    p['items'] = news.filter(sticky=False)
    p['news_feeds'] = NewsFeed.objects.order_by('title')
    return render_to_response(TEMPLATE_PATH + "news.html", p,
                              context_instance=RequestContext(req))
