from django.db import models
from django.utils.html import format_html


class NameModelMixin(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class PositiveIntegerModelMixin(models.Model):
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.number

    class Meta:
        abstract = True


# Марка транспорта
class Marks(NameModelMixin):
    class Meta:
        verbose_name = 'марка'
        verbose_name_plural = 'Марка мотоцикла'


# Модель транспорта
class Moto_models(NameModelMixin):
    class Meta:
        verbose_name = 'модель'
        verbose_name_plural = 'Модель мотоцикла'


# Тип двигателя
class Engine(NameModelMixin):
    class Meta:
        verbose_name = 'двигатель'
        verbose_name_plural = 'Тип двигателя'


# Кол-во цилиндров
class Cylinder_amount(NameModelMixin):
    class Meta:
        verbose_name_plural = 'Кол-во цилидров в двигателе'


# механизм системы газораспределения
class Gear(NameModelMixin):
    class Meta:
        verbose_name_plural = 'Механизм системы газораспределения'


# Тип мотоцикла
class Moto_type(NameModelMixin):
    class Meta:
        verbose_name_plural = 'Тип мотоцикла'


# Тактов
class Stroke_amount(NameModelMixin):
    class Meta:
        verbose_name_plural = 'Тактов'


# Кол-во передач
class Transmission(NameModelMixin):
    class Meta:
        verbose_name_plural = 'Трансмиссия'


# Объем двигателя в см3
class Displacement(PositiveIntegerModelMixin):
    class Meta:
        verbose_name = 'значение'
        verbose_name_plural = 'Объем двигателя в см3'


# Основное объявление мототранспорта
class Motorcycles(models.Model):
    status = models.BooleanField(default=False)
    # saleId - внутренний уникальный номер для парсинга с auto.ru
    mark_info = models.ForeignKey(Marks, on_delete=models.CASCADE)
    model_info = models.ForeignKey(Moto_models, on_delete=models.CASCADE)
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE)
    displacement = models.ForeignKey(Displacement, on_delete=models.CASCADE)
    cylinder_amount = models.ForeignKey(Cylinder_amount, on_delete=models.CASCADE)
    gear = models.ForeignKey(Gear, on_delete=models.CASCADE)
    horse_power = models.PositiveSmallIntegerField()
    moto_type = models.ForeignKey(Moto_type, on_delete=models.CASCADE)
    stroke_amount = models.ForeignKey(Stroke_amount, on_delete=models.CASCADE)
    transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Мотоцикл'
        verbose_name_plural = 'Мотоциклы'


class Motorcycle_images(models.Model):
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Motorcycles, on_delete=models.CASCADE)

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="150" height="150" />'.format(self.image.url))
