from django import forms
from django.conf import settings
from django.core.mail import EmailMessage

from .models import ContactRequest


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'content']

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        content = self.cleaned_data['content']
        email_message = EmailMessage(
            subject=f"New contact request from {name}",
            body=content,
            from_email=email,
            to=[settings.DEFAULT_TO_EMAIL],
            reply_to=[email]
        )
        email_message.send()
