from django.contrib import admin
from .models import Category, News


class NewsAdminView(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_category', 'author', 'created_at')
    list_display_links = ('id', 'title', )
    ordering = ('created_at', )
    filter_horizontal = ('category',)


# Register your models here.
admin.site.register(Category)
admin.site.register(News, NewsAdminView)