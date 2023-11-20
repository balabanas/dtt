from django.contrib import admin

from blog.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "snippet", "pub_dttm", "author", "online")
    prepopulated_fields = {"slug": ("title", )}


admin.site.register(Article, ArticleAdmin)
