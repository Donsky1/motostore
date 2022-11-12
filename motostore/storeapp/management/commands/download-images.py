from django.core.management.base import BaseCommand
import urllib.request
import shutil
import os


class Command(BaseCommand):
    help = 'Скачивание изображений для объявлений о продаже'

    def handle(self, *args, **options):
        self.stdout.write('скачивание картинок началось')

        # path to the images
        images_link = 'https://drive.google.com/u/0/uc?id=1HgCVr2njTsYUyVqsgO2zei4H3ZUr2s4P&export=download&confirm=t&uuid=51d1f5fa-7b11-4a43-b77f-e08640c1cd59&at=AHV7M3en7b390oRwe2C2FpNuGj1V:1668157636233'

        r = urllib.request.urlopen(images_link).read()

        with open('image.zip', 'wb') as archive:
            archive.write(r)

        if not os.path.exists(os.path.exists(os.path.join('motostore', 'media', 'images'))):
            os.mkdir('../motostore/media/images/')

        shutil.unpack_archive('image.zip', extract_dir=os.path.abspath(os.path.join('media', 'images')))

        if os.path.exists("image.zip"):
            os.remove("image.zip")

        self.stdout.write("pскачивание картинок закончилось", ending='')