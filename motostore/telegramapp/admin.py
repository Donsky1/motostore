from django.contrib import admin

from .models import TelegramRequest, TelegramUser


class TelegramRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'user', 'motorcycle_ids', 'uuid')
    list_display_links = ('id', 'chat_id', 'user', 'motorcycle_ids', 'uuid')


# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(TelegramRequest, TelegramRequestAdmin)