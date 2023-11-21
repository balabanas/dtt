from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse

from blog.models import Article


class TestArticleDetailView(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create(username="testuser")
        self.fullname_user = User.objects.create(username="testuser2", first_name="Name", last_name="Lastname")
        self.aoff: Article = Article.objects.create(title="Offline test title", content="test content",
                                                    author=self.user)
        self.aon: Article = Article.objects.create(title="Online test title", content="test content", online=True,
                                                   author=self.user)
        self.aon_fu: Article = Article.objects.create(title="Online test title", slug="test-title-online",
                                                      content="test content", online=True, author=self.fullname_user)
        self.aon_nl: Article = Article.objects.create(title="Blog post witn newline char in content",
                                                      content="test content\nnext line", online=True, author=self.user)

    def test_article_detail_view_online(self) -> None:
        response: TemplateResponse = self.client.get(
            reverse('article-detail', kwargs={'id': self.aon.id, 'slug': self.aon.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_detail.html')
        self.assertContains(response, 'Online test title')
        self.assertContains(response, 'test content')
        self.assertContains(response, self.user.username)

    def test_article_detail_view_offline(self) -> None:
        response: TemplateResponse = self.client.get(
            reverse('article-detail', kwargs={'id': self.aoff.id, 'slug': self.aoff.slug}))
        self.assertEqual(response.status_code, 404)

    def test_article_detail_view_display_user_fullname_with_username_fallback(self):
        response = self.client.get(reverse('article-detail', kwargs={'id': self.aon_fu.id, 'slug': self.aon_fu.slug}))
        self.assertContains(response, self.fullname_user.get_full_name())
        self.assertNotContains(response, self.fullname_user.username)
        response: TemplateResponse = self.client.get(reverse('article-detail', kwargs={'id': self.aon.id, 'slug': self.aon.slug}))
        self.assertContains(response, self.user.username)

    def test_article_detail_view_new_line_rendered(self):
        response: TemplateResponse = self.client.get(reverse('article-detail', kwargs={'id': self.aon_nl.id, 'slug': self.aon_nl.slug}))
        self.assertContains(response, 'test content<br>next line')
