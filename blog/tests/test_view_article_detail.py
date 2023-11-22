from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.test import TestCase

from blog.models import Article


class TestArticleDetailView(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create(username="testuser")
        self.fullname_user = User.objects.create(username="testuser2", first_name="Name", last_name="Lastname")
        self.aoff: Article = Article.objects.create(title="Offline test title", slug="offline-test-title",
                                                    content="test content", author=self.user)
        self.aon: Article = Article.objects.create(title="Online test title", slug="online-test_title",
                                                   content="test content", online=True,
                                                   author=self.user)
        self.aon_fu: Article = Article.objects.create(title="Online test title", slug="online-test-title-fu",
                                                      content="test content", online=True, author=self.fullname_user)

    def test_article_detail_view_online(self) -> None:
        response: TemplateResponse = self.client.get(self.aon.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_detail.html')
        self.assertContains(response, 'Online test title')
        self.assertContains(response, 'test content')
        self.assertContains(response, self.user.username)

    def test_article_detail_view_offline(self) -> None:
        response: TemplateResponse = self.client.get(self.aoff.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_article_detail_view_display_user_fullname_with_username_fallback(self):
        response = self.client.get(self.aon_fu.get_absolute_url())
        self.assertContains(response, self.fullname_user.get_full_name())
        self.assertNotContains(response, self.fullname_user.username)
        response: TemplateResponse = self.client.get(self.aon.get_absolute_url())
        self.assertContains(response, self.user.username)
