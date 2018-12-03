from widgeter.base import Widget
from widgeter.registry import registry
from news.models import NewsItem

class NewsWidget(Widget):
    template = 'news/home_widget.html'
    block = 'home'
    priority = 1

    def get_context(self, context, user):
        news = NewsItem.objects.filter(published=True).order_by('-publish_date')
        sticky_news = news.filter(sticky=True)[:6]
        if len(sticky_news) >= 6:
            recent_news = news.none()
        else:
            recent_news = news.filter(sticky=False)[:6-len(sticky_news)]

        return {
            'recent_news': recent_news,
            'sticky_news': sticky_news
        }

registry.register('news', NewsWidget())
