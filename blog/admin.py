from django.contrib import admin

from blog.models import Article, ContactRequest


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "snippet", "pub_dttm", "author", "online")
    prepopulated_fields = {"slug": ("title",)}


class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "pub_dttm",)


admin.site.register(Article, ArticleAdmin)
admin.site.register(ContactRequest, ContactRequestAdmin)
