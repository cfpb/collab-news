from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now
from random import randint

from django_webtest import WebTest

from models import NewsFeed, NewsItem
from widgets import NewsWidget


def create_news_items(is_sticky=False, amount=1):
    for i in range(0, amount):
        item = NewsItem(title='silly news item name',
                        publish_date=now(),
                        published=True,
                        create_user_id=1,
                        feed_id=randint(1, 2),
                        sticky=is_sticky)
        item.save()


class NewsFeedTest(TestCase):

    def test_slugify_on_save(self):
        feed = NewsFeed(title="My Special Feed")
        feed.save()
        self.assertEquals(feed.slug, 'my-special-feed')


class NewsItemTest(TestCase):
    fixtures = ['core-test-fixtures', 'news_fixtures.json']

    def test_slugify_on_save(self):
        item = NewsItem(title="My News Item",
                        publish_date=now(),
                        create_user_id=1,
                        feed_id=1)
        item.save()
        self.assertEquals(item.slug, 'my-news-item')


class NewsItemsTest(WebTest):
    fixtures = ['core-test-fixtures', 'news_fixtures.json']

    def test_news_access(self):
        response = self.client.get(reverse('news:list'))
        self.assertEquals(302, response.status_code)

    def test_get_news(self):
        self.client.login(username='test1@example.com', password='1')
        response = self.client.get(reverse('news:list'))
        self.assertContains(response, "Bat boy discovered", status_code=200)


class NewsWidgetViewTest(TestCase):
    def setUp(self):
        create_news_items(is_sticky=False, amount=7)
        feed = NewsFeed(title='second feed')
        feed.save()
        self.widget = NewsWidget()

    def test_no_stickies(self):
        response = self.widget.get_context(None, None)
        self.assertEquals(len(response['recent_news']), 6)
        self.assertEquals(len(response['sticky_news']), 0)

    def test_one_sticky(self):
        create_news_items(is_sticky=True, amount=1)
        response = self.widget.get_context(None, None)
        self.assertEquals(len(response['recent_news']), 5)
        self.assertEquals(len(response['sticky_news']), 1)

    def test_six_stickies(self):
        create_news_items(is_sticky=True, amount=6)
        response = self.widget.get_context(None, None)
        self.assertEquals(len(response['recent_news']), 0)
        self.assertEquals(len(response['sticky_news']), 6)

    def test_seven_stickies(self):
        create_news_items(is_sticky=True, amount=7)
        response = self.widget.get_context(None, None)
        self.assertEquals(len(response['recent_news']), 0)
        self.assertEquals(len(response['sticky_news']), 6)

