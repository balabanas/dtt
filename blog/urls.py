from django.urls import path

from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='blog-home'),
    path('<int:id>-<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail'),
]
