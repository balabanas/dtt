from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Article


class ArticleTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user('testuser')
        Article.objects.create(title='Test Article', slug='test-article', content='Test content', author=self.user)

    def test_article_retrieve(self) -> None:
        a: Article = Article.objects.get(title='Test Article')
        self.assertEqual(a.slug, 'test-article')
        self.assertEqual(a.content, 'Test content')
        self.assertEqual(a.author.username, self.user.username)
        self.assertFalse(a.online)
        self.assertEqual(a.__str__(), "Test Article")
        self.assertEqual(a.snippet(), "Test content...")

    def test_article_update(self) -> None:
        a: Article = Article.objects.get(title="Test Article")
        a.title = "new title"
        a.slug = "new-title"
        a.content = "new content"
        a.online = True
        a.save()
        self.assertEqual(a.title, "new title")
        self.assertEqual(a.slug, "new-title")
        self.assertEqual(a.content, "new content")
        self.assertEqual(a.online, True)

    def test_article_delete(self) -> None:
        a: Article = Article.objects.get(title="Test Article")
        a.delete()
        self.assertEqual(Article.objects.count(), 0)
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(title="Test Article")

    def test_article_slug_made_unique(self) -> None:
        """Attemts to add 2 more articles with the same slug"""
        a: Article = Article.objects.create(title="Test Article", slug="test-article", content="Test content", author=self.user)
        a.slug = "test-title-"
        b: Article = Article.objects.create(title="Test Article", slug="test-article", content="Test content", author=self.user)
        b.slug = "test-title--"

