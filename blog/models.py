from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def validate_charfield_not_empty(value: str):
    if value.strip() == "":
        raise ValidationError("This field cannot be empty or blanks-only")
    return value


class Article(models.Model):
    title = models.CharField(max_length=100, blank=False, validators=[validate_charfield_not_empty])
    slug = models.SlugField(unique=True, blank=False)
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pub_dttm = models.DateTimeField(auto_now_add=True)
    online = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    def snippet(self) -> str:
        try:  # will have issue if content is NULL
            return self.content[:50] + '...'
        except TypeError:
            return "(empty yet)"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        while Article.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug += "-"  # altering slug until it is unique
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('article-detail', kwargs={'id': self.id, 'slug': self.slug})


class ContactRequest(models.Model):
    name = models.CharField(max_length=100, blank=False, validators=[validate_charfield_not_empty])
    email = models.EmailField(blank=False)
    content = models.TextField(blank=False, validators=[validate_charfield_not_empty])
    pub_dttm = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name + " " + self.pub_dttm.strftime("%Y-%m-%d %H:%M:%S")
