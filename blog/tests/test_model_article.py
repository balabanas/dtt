import time

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from blog.models import Article


class ArticleTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user('testuser')
        self.a = Article.objects.create(title='Test Article', slug='test-article', content='Test content',
                                        author=self.user)

    def test_article_retrieve(self) -> None:
        a: Article = Article.objects.get(title='Test Article')
        self.assertEqual(a.slug, 'test-article')
        self.assertEqual(a.content, 'Test content')
        self.assertEqual(a.author.username, self.user.username)
        self.assertFalse(a.online)
        self.assertEqual(a.__str__(), "Test Article")
        self.assertEqual(a.snippet, "Test content...")

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

    def test_article_user_required(self):
        with self.assertRaises(IntegrityError):
            Article.objects.create(title="Article With No User Specified", slug="test-title", content="test content")

    def test_article_title_required(self):
        a1: Article = Article(title="  ", content="just content", author=self.user)
        a2: Article = Article(content="just content", author=self.user)
        with self.assertRaises(ValidationError) as error1:
            a1.full_clean()
        with self.assertRaises(ValidationError) as error2:
            a2.full_clean()
        msg1: str = error1.exception.message_dict['title'][0]
        msg2: str = error2.exception.message_dict['title'][0]
        self.assertTrue(all(word in msg1 for word in ['empty', 'blanks']))
        self.assertTrue(all(word in msg2 for word in ['cannot', 'blank']))

    def test_article_title_max_length(self):
        a: Article = Article(title="test title" * 100, slug="test-title", content="test content", author=self.user)
        with self.assertRaises(ValidationError) as error:
            a.full_clean()
        msg: str = error.exception.message_dict['title'][0]
        self.assertTrue(all(word in msg for word in ['at most', 'characters']))

    def test_article_content_nullable(self):
        Article.objects.create(title="Test Article 2", slug="test-title-2", author=self.user)
        self.assertEqual(Article.objects.count(), 2)  # article with no content is successfully created

    def test_article_pub_dttm_order(self):
        time.sleep(0.01)  # wait 0.01 second to make sure the pub_dttm is different from self.a
        a: Article = Article.objects.create(title="Later Article", slug="test-title", content="test content",
                                            author=self.user)
        self.assertGreater(a.pub_dttm, self.a.pub_dttm)

    def test_article_content_empty(self) -> None:
        article: Article = Article.objects.create(title="Article w Empty Content", slug="article-w-empty-content",
                                                  author=self.user)
        self.assertEqual(article.snippet, "(empty yet...)")
