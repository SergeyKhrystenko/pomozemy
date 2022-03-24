from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.pk}){self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Fundraiser(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField()
    purpose = models.PositiveIntegerField()
    active = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    votes_positive = models.PositiveIntegerField()
    votes_negative = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'({self.pk}){self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Fundraiser, self).save(*args, **kwargs)


class Transaction(models.Model):
    fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    message = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
