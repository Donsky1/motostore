from django.contrib import admin

from . import models


class PhotoInLine(admin.StackedInline):
    model = models.Motorcycle_images
    extra = 1
    fields = ('image_tag', 'moto', 'image', )
    readonly_fields = ('image_tag',)
    show_change_link = True


@admin.action(description='Опубликовать (status=True)')
def set_active(modeladmin, request, queryset):
    queryset.update(status=True)


@admin.action(description='Снять с публикации (status=False)')
def unset_active(modeladmin, request, queryset):
    queryset.update(status=False)


class MotorcycleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Motorcycle._meta.get_fields()
                    if field.name != 'motorcycle_images' if field.name != 'comment']
    list_display_links = ['id', 'mark_info', ]
    list_editable = ('status',)
    list_filter = ('model_info', 'mark_info', 'moto_type')
    readonly_fields = ('rate',)
    ordering = ('updated_at',)
    actions = [set_active, unset_active]
    list_per_page = 30
    search_fields = ('mark_info__name', 'model_info__name', 'moto_type__name',
                     'horse_power', 'displacement__number', 'color__name', 'city__name')
    fieldsets = (
        (None, {'fields': ('status', 'rate')}),
        ('Базовая информация', {'fields':
                                    ('mark_info', 'model_info', 'moto_type', 'displacement', 'horse_power', 'color',
                                     'transmission'),
                                'description': 'Базовая информация о мотоцикле, которую необходимо заполнить обязательно'}),
        ('Дополнительная информация', {'fields': ('city', 'mileage', 'user', 'comment')}),
        ('Цена', {'fields': ('price', ), 'classes': ('wide', 'extrapretty')})
    )
    inlines = [PhotoInLine]


class ColorAdmin(admin.ModelAdmin):
    fields = (('name', 'color_hex'), 'color_view_')
    readonly_fields = ('color_view_',)
    list_display = ('id', 'name', 'color_hex', 'color_view')
    list_display_links = ('id', 'name', 'color_hex', 'color_view')


class Motorcycle_imagesAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'image', 'moto')
    readonly_fields = ('image_tag',)
    list_display = ('moto', 'image')
    list_display_links = ('moto',)
    list_per_page = 30


class TypeModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'translate')
    list_display_links = ('id', 'name', 'translate')


class TransmissionlAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'translate')
    list_display_links = ('id', 'name', 'translate')


admin.site.register(models.Marks)
admin.site.register(models.Moto_models)
admin.site.register(models.Moto_type, TypeModelAdmin)
admin.site.register(models.Color, ColorAdmin)
admin.site.register(models.City)
admin.site.register(models.Transmission, TransmissionlAdmin)
admin.site.register(models.Displacement)
admin.site.register(models.Motorcycle, MotorcycleAdmin)
admin.site.register(models.Motorcycle_images, Motorcycle_imagesAdmin)
