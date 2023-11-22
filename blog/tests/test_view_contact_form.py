import datetime
from unittest.mock import patch

from django.conf import settings
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import ContactRequest


class ContactFormViewTest(TestCase):
    def setUp(self) -> None:
        self.dttm_before_send: datetime.datetime = timezone.now()
        self.form_data: dict[str: str, ] = {
            'name': 'My Name',
            'email': 'test@test.com',
            'content': 'Test message',
        }

    def test_contact_form_view_form_sent(self) -> None:
        response: HttpResponseRedirect = self.client.post(reverse('contact-form'), self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('blog-home'))

    def test_contact_form_view_form_saved_with_dttm(self) -> None:
        self.client.post(reverse('contact-form'), self.form_data)
        self.assertEqual(1, ContactRequest.objects.count())
        contact_request: ContactRequest = ContactRequest.objects.first()
        self.assertGreater(contact_request.pub_dttm, self.dttm_before_send)

    @patch('blog.views.EmailMessage')
    def test_contact_form_view_send_email_method(self, mock_email_message) -> None:
        self.client.post(reverse('contact-form'), self.form_data)
        mock_email_message.assert_called_once_with(
            subject=f"New contact request from {self.form_data['name']}",
            body=self.form_data['content'],
            from_email=self.form_data['email'],
            to=[settings.DEFAULT_TO_EMAIL],
            reply_to=[self.form_data['email']]
        )
        mock_email_message.return_value.send.assert_called_once()
