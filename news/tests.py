from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now

from django_webtest import WebTest

from models import NewsFeed, NewsItem


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
