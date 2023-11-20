from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from blog.models import Article


class TestArticleListView(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create(username="testuser")
        Article.objects.create(title="Offline test title", slug="test-title", content="test content",
                               author=self.user)
        Article.objects.create(title="Online test title", slug="test-title", content="test content",
                               online=True, author=self.user)

    def test_article_list_view(self) -> None:
        response: HttpResponse = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_list.html')
        self.assertContains(response, 'Online test title')
        self.assertContains(response, 'test content...')
        self.assertContains(response, self.user.username)
