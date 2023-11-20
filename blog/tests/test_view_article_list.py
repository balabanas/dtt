from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from blog.models import Article
from blog.views import ArticleListView


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


class ArticlePaginationTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", password="12345")
        for i in range(14):
            Article.objects.create(title=f"Online test title {i + 1}", slug=f"test-title- {i + 1}",
                                   content=f"test content {i + 1}", online=True, author=user)

    def test_pagination_first_page(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_list.html')
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), ArticleListView.paginate_by)

    def test_pagination_second_page(self):
        response = self.client.get(reverse('blog-home') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), ArticleListView.paginate_by)

    def test_invalid_page_number(self):
        response = self.client.get(reverse('blog-home') + '?page=invalid')
        self.assertEqual(response.status_code, 404)
