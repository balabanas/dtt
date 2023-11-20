from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from blog.forms import ContactForm
from blog.models import Article

ARTICLE_PAGINATION_SIZE = 5


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = ARTICLE_PAGINATION_SIZE
    queryset = Article.objects.filter(online=True).order_by('-pub_dttm')  # todo: +model manager?


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    queryset = Article.objects.filter(online=True)


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'blog/contact_form.html'
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.save()
        form.send_email()
        return super().form_valid(form)
