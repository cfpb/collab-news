from widgeter.base import Widget
from widgeter.registry import registry
from news.models import NewsItem

class NewsWidget(Widget):
    template = 'news/home_widget.html'
    block = 'home'
    priority = 1

    def get_context(self, context, user):
        return {
            'recent_news': NewsItem.objects.filter(published=True).order_by('-publish_date')[:3]
        }

registry.register('news', NewsWidget())
