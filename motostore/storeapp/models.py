from django.db import models
from django.utils import timezone
from django.utils.html import format_html


def offer_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    return 'images/{0}/{1}'.format(instance.moto.id, filename)


class NameModelMixin(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


# Марка транспорта, к примеру Yamaha
class Marks(NameModelMixin):
    class Meta:
        verbose_name = 'марка'
        verbose_name_plural = 'Марка мотоцикла'


# Модель транспорта, к примеру XJ6
class Moto_models(NameModelMixin):
    class Meta:
        verbose_name = 'модель'
        verbose_name_plural = 'Модель мотоцикла'


# Тип мотоцикла, к примеру спорттуризм
class Moto_type(NameModelMixin):
    class Meta:
        verbose_name_plural = 'Тип мотоцикла'


class Color(NameModelMixin):
    color_hex = models.CharField(max_length=7)

    class Meta:
        verbose_name_plural = 'Цвет транспорта'

    def color_view_(self):
        if self.color_hex:
            return format_html('<table border="1" cellspacing="0" width="270px" height="30px"><tr><td colspan="2" '
                               'bgcolor="#{}" align="center"></td></tr></table>'.format(self.color_hex))

    def color_view(self):
        if self.color_hex:
            return format_html('<table border="1" cellspacing="0" width="20px"'
                               'height="18px"><tr><td colspan="2" '
                               'bgcolor="#{}"</td></tr></table>'.format(self.color_hex))


class City(NameModelMixin):
    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'Города'


# Кол-во передач, к примеру 6 ступенчатая
class Transmission(NameModelMixin):
    class Meta:
        verbose_name_plural = 'Трансмиссия'


class Displacement(models.Model):
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Объем двигателя в см3'
        verbose_name_plural = 'Объем двигателя в см3'


# Основное объявление мототранспорта
class Motorcycle(models.Model):
    status = models.BooleanField(default=False)
    # saleId - внутренний уникальный номер для парсинга с auto.ru
    mark_info = models.ForeignKey(Marks, on_delete=models.CASCADE, verbose_name='Марка')
    model_info = models.ForeignKey(Moto_models, on_delete=models.CASCADE, verbose_name='Модель')
    moto_type = models.ForeignKey(Moto_type, on_delete=models.CASCADE, verbose_name='Тип транспорта')
    displacement = models.ForeignKey(Displacement, on_delete=models.CASCADE, verbose_name='Объем двигателя, см3')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name='Цвет транспорта')
    mileage = models.PositiveIntegerField(verbose_name='Километраж')
    horse_power = models.PositiveSmallIntegerField(verbose_name='Мощность, л.с')
    price = models.PositiveIntegerField(verbose_name='Цена')
    transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE, verbose_name='Коробка передач')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    comment = models.TextField(default='не указано ...', verbose_name='Комментарий')

    def __str__(self):
        return '{} {} _ID: {}'.format(self.mark_info, self.model_info, self.id)

    class Meta:
        verbose_name = 'Мотоцикл'
        verbose_name_plural = 'Мотоциклы'


class Motorcycle_images(models.Model):
    image = models.ImageField(upload_to=offer_directory_path)
    moto = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="150" height="150" />'.format(self.image.url))
