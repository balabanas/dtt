from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    content = models.TextField(blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pub_dttm = models.DateTimeField(auto_now_add=True)
    online = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    @property
    def snippet(self) -> str:
        if self.content:
            return self.content[:50] + '...'
        return '(empty yet...)'

    def get_absolute_url(self) -> str:
        return reverse('article-detail', kwargs={'id': self.id, 'slug': self.slug})


class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    pub_dttm = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name + " " + self.pub_dttm.strftime("%Y-%m-%d %H:%M:%S")
