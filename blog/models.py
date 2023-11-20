from django.db import models
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(unique=True, blank=False)
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    online = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.content[:50] + '...'

    def save(self, *args, **kwargs):
        while Article.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug += "-"  # altering slug until it is unique
        super().save(*args, **kwargs)
