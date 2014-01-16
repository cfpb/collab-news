from django.contrib import admin
from news.models import FeedSubscription, NewsItem, NewsFeed

admin.site.register(FeedSubscription)
admin.site.register(NewsFeed)
admin.site.register(NewsItem)
