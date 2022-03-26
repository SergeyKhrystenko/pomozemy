from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField


class StaticPage(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    body = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.pk}){self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(StaticPage, self).save(*args, **kwargs)
