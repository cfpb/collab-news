from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify

from collab.settings import AUTH_USER_MODEL


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
    sticky = models.BooleanField(default=False)
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


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s, %s" % (obj.last_name, obj.first_name)


class NewsItemAdminForm(forms.ModelForm):
    create_user = CustomModelChoiceField(
        queryset=get_user_model().objects.order_by(
            'last_name', 'first_name'
        ).filter(is_active=True).exclude(first_name='', last_name='')
    )

    class Meta:
        model = NewsItem


class NewsItemAdmin(admin.ModelAdmin):
    form = NewsItemAdminForm


class FeedSubscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL)
    feed = models.ForeignKey('NewsFeed')
