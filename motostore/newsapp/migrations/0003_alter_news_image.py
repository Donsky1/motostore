# Generated by Django 4.0.6 on 2022-09-12 18:32

from django.db import migrations, models
import newsapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0002_alter_category_options_alter_news_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, upload_to=newsapp.models.news_directory_path),
        ),
    ]
