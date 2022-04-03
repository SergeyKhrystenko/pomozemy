from django.db import models
from django.db.models import Sum
from django.utils.text import slugify
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    slug = models.SlugField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Fundraiser(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    slug = models.SlugField(max_length=50)
    description = HTMLField(verbose_name=_('Description'))
    purpose = models.PositiveIntegerField(verbose_name=_('Purpose'))
    active = models.BooleanField(default=False, verbose_name=_('Active'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name=_('Start Date'))
    end_date = models.DateTimeField(verbose_name=_('End Date'))
    votes_positive = models.PositiveIntegerField(default=0)
    votes_negative = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.pk}){self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Fundraiser, self).save(*args, **kwargs)

    def transaction_sum(self):
        return self.transaction_set.all().aggregate(Sum('amount'))['amount__sum'] or 0

    def upvote(self):
        self.votes_positive += 1
        self.save()

    def downvote(self):
        self.votes_negative += 1
        self.save()


class Transaction(models.Model):
    fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=True, verbose_name=_('Comment'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def get_user_name(self):
        if self.user:
            return self.user.get_full_name()
        return 'Anonymous'


class Comment(models.Model):
    message = models.CharField(max_length=500, verbose_name=_('Message'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_user_name(self):
        if self.user:
            return self.user.get_full_name()
        return 'Anonymous'
