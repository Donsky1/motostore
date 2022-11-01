from django.contrib import admin

from . import models


class PhotoInLine(admin.StackedInline):
    model = models.Motorcycle_images


class MotorcycleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Motorcycle._meta.get_fields()
                    if field.name != 'motorcycle_images' if field.name != 'comment']
    list_display_links = ['id', 'mark_info', ]
    inlines = [PhotoInLine]
    list_editable = ('status',)
    list_filter = ('city', )
    readonly_fields = ('rate', )
    ordering = ('updated_at', )


class ColorAdmin(admin.ModelAdmin):
    fields = ('name', 'color_hex', 'color_view_')
    readonly_fields = ('color_view_',)
    list_display = ('id', 'name', 'color_hex', 'color_view')
    list_display_links = ('id', 'name', 'color_hex', 'color_view')


class Motorcycle_imagesAdmin(admin.ModelAdmin):
    list_display = ('image', 'moto')
    list_display_links = ('image', 'moto')


class TypeModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(models.Marks)
admin.site.register(models.Moto_models)
admin.site.register(models.Moto_type, TypeModelAdmin)
admin.site.register(models.Color, ColorAdmin)
admin.site.register(models.City)
admin.site.register(models.Transmission)
admin.site.register(models.Displacement)
admin.site.register(models.Motorcycle, MotorcycleAdmin)
admin.site.register(models.Motorcycle_images, Motorcycle_imagesAdmin)
