from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from blog.forms import ContactForm


class ContactFormTestCase(TestCase):
    @patch('blog.forms.EmailMessage')
    def test_send_email(self, mock_email_message):
        name = 'User Name'
        email = 'my@test.com'
        content = 'This is a test message.'

        form = ContactForm(data={
            'name': name,
            'email': email,
            'content': content
        })
        form.is_valid()
        form.send_email()

        mock_email_message.assert_called_once_with(
            subject=f"New contact request from {name}",
            body=content,
            from_email=email,
            to=[settings.DEFAULT_TO_EMAIL],
            reply_to=[email]
        )
        mock_email_message.return_value.send.assert_called_once()
