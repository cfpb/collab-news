from django.conf.urls import patterns, url


urlpatterns = patterns('news.views',
                       url(r'^$', 'news_list', name='list'),
                       url(r'^feed/(?P<slug>.*)/$',
                           'news_list', name='feed'),
                       url(r'^(?P<slug>.*)/$', 'news_item', name='item'),
                       )
