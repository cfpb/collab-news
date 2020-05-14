from django.contrib import admin
from news.models import FeedSubscription, NewsFeed, NewsItem, NewsItemAdmin

admin.site.register(FeedSubscription)
admin.site.register(NewsFeed)
admin.site.register(NewsItem, NewsItemAdmin)
