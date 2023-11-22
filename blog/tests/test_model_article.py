import time

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from blog.models import Article


class ArticleTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user('testuser')
        self.article: Article = Article.objects.create(title='Test Article', slug='test-article',
                                                       content='Test content', author=self.user)

    def test_article_retrieve(self) -> None:
        article: Article = Article.objects.get(title='Test Article')
        self.assertEqual(article.slug, 'test-article')
        self.assertEqual(article.content, 'Test content')
        self.assertEqual(article.author.username, self.user.username)
        self.assertFalse(article.online)
        self.assertIsNotNone(article.pub_dttm)
        self.assertEqual(str(article), "Test Article")
        self.assertEqual(article.snippet, "Test content...")

    def test_article_update(self) -> None:
        article: Article = Article.objects.get(title="Test Article")
        article.title = ""
        article.slug = ""
        article.content = ""
        article.online = True
        article.save()
        self.assertEqual(article.title, "")
        self.assertEqual(article.slug, "")
        self.assertEqual(article.content, "")
        self.assertEqual(article.online, True)

    def test_article_delete(self) -> None:
        article: Article = Article.objects.get(title="Test Article")
        article.delete()
        self.assertEqual(Article.objects.count(), 0)

    def test_article_user_cascade_deletion(self):
        User.objects.get(username='testuser').delete()
        self.assertEqual(Article.objects.count(), 0)

    def test_article_title_max_length(self) -> None:
        article: Article = Article(title="x" * 101, author=self.user)
        with self.assertRaises(ValidationError) as error:
            article.full_clean()
        msg: str = error.exception.message_dict['title'][0]
        self.assertTrue(all(word in msg for word in ['at most', 'characters']))

    def test_article_pub_dttm_order(self) -> None:
        time.sleep(0.01)  # wait 0.01 second to make sure the pub_dttm is different from self.article
        article: Article = Article.objects.create(title="Later Article", slug="test-title", content="test content",
                                                  author=self.user)
        self.assertGreater(article.pub_dttm, self.article.pub_dttm)

    def test_article_content_empty(self) -> None:
        article: Article = Article.objects.create(title="Article w Empty Content", slug="article-w-empty-content",
                                                  author=self.user)
        self.assertEqual(article.snippet, "(empty yet...)")

    def test_article_get_absolute_url(self) -> None:
        self.assertEqual(self.article.get_absolute_url(), f"/blog/{self.article.id}-test-article/")
