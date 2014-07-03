from django.db import models
from collab.settings import AUTH_USER_MODEL
from django.template.defaultfilters import slugify


class NewsFeed(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, editable=False)

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.slug = slugify(self.title)
        super(NewsFeed, self).save(*args, **kwargs)


class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, editable=False)
    body = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField()
    published = models.BooleanField(default=False)
    create_user = models.ForeignKey(AUTH_USER_MODEL)
    feed = models.ForeignKey('NewsFeed')

    def __unicode__(self):
        return u'%s' % (self.title)

    def get_absolute_url(self):
        return "/news/%s/" % (self.slug)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.slug = self._generate_slug(self.title)
        super(NewsItem, self).save(*args, **kwargs)

    def _generate_slug(self, title):
        slugify_val = slugify(title)
        slug = slugify_val
        next = 2
        qs = NewsItem.objects.all()
        while qs.filter(slug=slug).count() > 0:
            slug = slugify_val + "-" + str(next)
            next += 1
        return slug

    # Search fields
    @classmethod
    def search_category(cls):
        return 'News'

    @property
    def to_search_result(self):
        return self.title


class FeedSubscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL)
    feed = models.ForeignKey('NewsFeed')
