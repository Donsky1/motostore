from django.contrib import admin
from .models import StoreAppUser


class StoreAppUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_authenticated', 'is_superuser', 'is_author')
    list_display_links = ('id', 'username', 'is_authenticated', 'is_superuser', 'is_author')
    ordering = ['id']


admin.site.register(StoreAppUser, StoreAppUserAdmin)
