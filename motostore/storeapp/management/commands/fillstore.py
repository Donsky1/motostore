from django.core.management.base import BaseCommand
from storeapp.management.config import cookies, headers
from storeapp.management.parsing import Parsing

import requests


class Command(BaseCommand):
    help = 'Parsing ads with motorcycles sales from auto.ru ' \
           'You have need to add config file. ' \
           'In this config file you must have cookies, headers from inspector code your browser' \
           '(F12 - Network - listing/ - copy). Before parsing need to add superuser.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-w',
            '--wait',
            action='store_true',
            default=False,
            help='Время ожидания между запросами. Если не указать, то рандом значение. '
        )
        parser.add_argument('wait_time', nargs='?', default=False, type=int)

    def handle(self, *args, **options):
        self.stdout.write('parsing start')

        wait_params = options['wait_time'] if options['wait'] and options['wait_time'] else False

        # можно большую часть запросов адресовать админ запросу
        json_data = {
            'year_from': 2000,
            'year_to': 2022,
            'price_from': 1,
            'price_to': 9999999,
            'displacement_from': 50,
            'displacement_to': 1800,
            'catalog_filter': [
                # для упрощения можно менять только этот список
                # {
                #     'mark': 'YAMAHA',
                #     'model': 'MT_03',
                # },
                {
                    'mark': 'KTM',
                    'model': '125_DUKE',
                },
                {
                    'mark': 'KTM',
                    'model': '125_SX',
                },
                {
                    'mark': 'KTM',
                    'model': '1290_SUPER_ADVENTURE_R',
                },
                {
                    'mark': 'KTM',
                    'model': '1290_SUPER_ADVENTURE_S',
                },
                {
                    'mark': 'KTM',
                    'model': '1290_SUPER_DUKE_GT',
                },
                {
                    'mark': 'KTM',
                    'model': '1290_SUPER_DUKE_R',
                },
                {
                    'mark': 'KTM',
                    'model': 'ADVENTURE',
                },

            ],
            'moto_category': 'MOTORCYCLE',
            # group: used, new, all
            'section': 'used',
            'category': 'moto',
            'output_type': 'list',
            'page': 1
        }

        motorcycles = Parsing('https://auto.ru/-/ajax/desktop/listing/', json_data=json_data,
                              cookies=cookies, headers=headers)
        motorcycles.fill_db(wait_params=wait_params)

        self.stdout.write("parsing end", ending='')
