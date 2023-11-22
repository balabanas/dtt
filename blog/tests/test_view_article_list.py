from django.contrib.auth.models import User
from django.template.response import TemplateResponse
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
        response: TemplateResponse = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_list.html')
        self.assertContains(response, 'Online test title')
        self.assertContains(response, 'test content...')
        self.assertContains(response, self.user.username)

    def test_article_list_view_offline(self) -> None:
        response: TemplateResponse = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Offline test title')

    def test_article_list_view_slash_redirects(self) -> None:
        response: TemplateResponse = self.client.get('/blog')
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, '/blog/', status_code=301, target_status_code=200)


class ArticlePaginationTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="testuser", password="12345")
        for i in range(14):
            Article.objects.create(title=f"Online test title {i + 1}", slug=f"test-title-{i + 1}",
                                   content=f"test content {i + 1}", online=True, author=user)

    def test_pagination_first_page(self) -> None:
        response: TemplateResponse = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_list.html')
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), ArticleListView.paginate_by)

    def test_pagination_second_page(self) -> None:
        response: TemplateResponse = self.client.get(reverse('blog-home') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), ArticleListView.paginate_by)

    def test_invalid_page_number(self) -> None:
        response: TemplateResponse = self.client.get(reverse('blog-home') + '?page=invalid')
        self.assertEqual(response.status_code, 404)
