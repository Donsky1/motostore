from django.db import models
from userapp.models import StoreAppUser


def news_directory_path(instance, filename):
    return 'news/{0}/{1}/{2}'.format(instance.author, instance.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class News(models.Model):
    category = models.ManyToManyField(Category, verbose_name='Категория')
    title = models.CharField(max_length=250, unique=True, verbose_name='Заголовок')
    author = models.ForeignKey(StoreAppUser, on_delete=models.CASCADE, verbose_name='Автор')
    image = models.ImageField(upload_to=news_directory_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    text = models.TextField()
    link = models.URLField(blank=True, max_length=500, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def get_category(self):
        categories = self.category.all()
        return ', '.join([category.name for category in categories])