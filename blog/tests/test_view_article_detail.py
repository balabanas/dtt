from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase

from blog.models import Article


class TestArticleDetailView(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create(username="testuser", password="12345")
        self.aoff: Article = Article.objects.create(title="Offline test title", content="test content",
                                                    author=self.user)
        self.aon: Article = Article.objects.create(title="Online test title", content="test content", online=True,
                                                   author=self.user)

    def test_article_detail_view_online(self) -> None:
        response: HttpResponse = self.client.get(f'/blog/{self.aon.id}-{self.aon.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_detail.html')
        self.assertContains(response, 'Online test title')
        self.assertContains(response, 'test content')
        self.assertContains(response, self.user.username)
