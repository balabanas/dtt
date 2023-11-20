from django.views.generic import ListView, DetailView

from blog.models import Article

ARTICLE_PAGINATION_SIZE = 5


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = ARTICLE_PAGINATION_SIZE


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
