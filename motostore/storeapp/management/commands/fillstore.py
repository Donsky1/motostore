from django.core.management.base import BaseCommand
from storeapp.management.config import cookies, headers
from storeapp.management.parsing import Parsing

import requests


class Command(BaseCommand):
    help = 'Parsing ads with motorcycles sales from auto.ru'

    def handle(self, *args, **options):
        self.stdout.write('parsing start')

        json_data = {
            'year_from': 2000,
            'year_to': 2022,
            'price_from': 1,
            'price_to': 9999999,
            'displacement_from': 50,
            'displacement_to': 1800,
            'catalog_filter': [
                {
                    'mark': 'YAMAHA',
                    'model': 'XJ6',
                },
                # use a similar block if you want to add new group moto
                # {
                #     'mark': 'YAMAHA',
                #     'model': 'MT_03',
                # },
            ],
            'moto_category': 'MOTORCYCLE',
            # group: used, new, all
            'section': 'used',
            'category': 'moto',
            'output_type': 'list',
            'page': 1
        }

        motocycles = Parsing('https://auto.ru/-/ajax/desktop/listing/', json_data=json_data, cookies=cookies, headers=headers)
        motocycles.fill_db()

        self.stdout.write("parsing end", ending='')
