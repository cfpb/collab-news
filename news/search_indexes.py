import datetime
from haystack import indexes
from news.models import NewsItem
from django.utils.html import strip_tags


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    feed = indexes.CharField(model_attr='feed', null=True)
    user = indexes.CharField(model_attr='create_user')
    display = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='body')
    index_name = indexes.CharField(indexed=False)
    index_priority = indexes.IntegerField(indexed=False)
    url = indexes.CharField(indexed=False, null=True)
    index_sort = indexes.IntegerField(indexed=False, null=True)

    PRIORITY = 3

    def prepare_index_name(self, obj):
        return "Announcements"

    def prepare_index_priority(self, obj):
        return self.PRIORITY

    def prepare_url(self, obj):
        return obj.get_absolute_url()

    def get_model(self):
        return NewsItem

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(published=True)

    def prepare_description(self, obj):
        return "%s..." % (strip_tags(obj.body)[:100])
