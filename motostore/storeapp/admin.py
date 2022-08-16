from django.contrib import admin

from . import models


class PhotoInLine(admin.StackedInline):
    model = models.Motorcycle_images


class MotorcyclesAdmin(admin.ModelAdmin):
    inlines = [PhotoInLine]


admin.site.register(models.Marks)
admin.site.register(models.Moto_models)
admin.site.register(models.Engine)
admin.site.register(models.Cylinder_amount)
admin.site.register(models.Gear)
admin.site.register(models.Moto_type)
admin.site.register(models.Stroke_amount)
admin.site.register(models.Transmission)
admin.site.register(models.Displacement)
admin.site.register(models.Motorcycles, MotorcyclesAdmin)
