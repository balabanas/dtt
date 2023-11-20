from django.contrib import admin

from blog.models import Article, ContactRequest


class ArticleAdmin(admin.ModelAdmin):
    list_display: tuple[str, ] = ("title", "snippet", "pub_dttm", "author", "online")
    prepopulated_fields: dict = {"slug": ("title",)}


class ContactRequestAdmin(admin.ModelAdmin):
    list_display: tuple[str, ] = ("name", "email", "pub_dttm")

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request) -> bool:
        return False


admin.site.register(Article, ArticleAdmin)
admin.site.register(ContactRequest, ContactRequestAdmin)
