from django.db import models
from simple_history.models import HistoricalRecords


class StaticPage(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
