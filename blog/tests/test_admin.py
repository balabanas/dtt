from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase, RequestFactory

from blog.admin import ContactRequestAdmin, ArticleAdmin
from blog.models import ContactRequest, Article


class ArticleAdminTestCase(TestCase):
    def setUp(self):
        self.user: User = User.objects.create_user(username='test_admin', is_superuser=True)  # admin user
        self.factory: RequestFactory = RequestFactory()
        self.model_admin: ArticleAdmin = ArticleAdmin(Article, AdminSite())
        self.client.force_login(self.user)
        self.request: WSGIRequest = self.factory.get('/admin/blog/article/')
        self.request.user = self.user

    def test_has_change_permission(self) -> None:
        has_change: bool = self.model_admin.has_change_permission(request=self.request, obj={})
        self.assertTrue(has_change)


class ContactRequestAdminTestCase(TestCase):
    def setUp(self):
        self.user: User = User.objects.create_user(username='test_admin', is_superuser=True)  # admin user
        self.factory: RequestFactory = RequestFactory()
        self.model_admin: ContactRequestAdmin = ContactRequestAdmin(ContactRequest, AdminSite())
        self.client.force_login(self.user)
        self.request: WSGIRequest = self.factory.get('/admin/blog/contactrequest/')
        self.request.user = self.user

    def test_has_change_permission(self) -> None:
        has_change: bool = self.model_admin.has_change_permission(request=self.request, obj={})
        self.assertFalse(has_change)

    def test_has_add_permission(self) -> None:
        has_add: bool = self.model_admin.has_add_permission(request=self.request)
        self.assertFalse(has_add)
