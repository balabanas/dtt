from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from blog.models import Article, ContactRequest

ARTICLE_PAGINATION_SIZE = 5


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = ARTICLE_PAGINATION_SIZE
    queryset = Article.objects.filter(online=True).select_related('author').order_by('-pub_dttm')


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    queryset = Article.objects.filter(online=True)


class ContactFormView(CreateView):
    model: ContactRequest = ContactRequest
    fields: list[str, ] = ['name', 'email', 'content']
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form) -> HttpResponseRedirect:
        """Save instance, send email, and only then redirect"""
        result: HttpResponseRedirect = super().form_valid(form)
        self.send_email(form)
        return result

    @staticmethod
    def send_email(form) -> None:
        name: str = form.cleaned_data['name']
        email: str = form.cleaned_data['email']
        content: str = form.cleaned_data['content']
        email_message: EmailMessage = EmailMessage(
            subject=f"New contact request from {name}",
            body=content,
            from_email=email,
            to=[settings.DEFAULT_TO_EMAIL],
            reply_to=[email]
        )
        email_message.send()
