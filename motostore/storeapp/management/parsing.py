import requests
from lxml import html
import os
from tqdm import tqdm

from storeapp.models import Marks, Moto_models, Moto_type, Color, City, Transmission, Displacement, Motorcycle, \
    Motorcycle_images
from userapp.models import StoreAppUser


class Parsing:

    def __init__(self, api_url, json_data, cookies, headers):
        self.api_url = api_url
        self.json_data = json_data
        self.cookies = cookies
        self.headers = headers
        self.response = requests.post(api_url, cookies=cookies, headers=headers,
                                      json=json_data).json()

    def _get_new_requests_post(self):
        self.response = requests.post(self.api_url, cookies=self.cookies, headers=self.headers,
                                      json=self.json_data).json()

    def _get_total_info(self):
        return {
            'total_offers_count': self.response['pagination']['total_offers_count'],
            'total_page_count': self.response['pagination']['total_page_count'],
            'total_offers_on_page': len(self.response['offers'])
        }

    def _get_mark_info(self, moto_number):
        return self.response['offers'][moto_number]['vehicle_info']['mark_info']['code']

    def _get_model_info(self, moto_number):
        return self.response['offers'][moto_number]['vehicle_info']['model_info']['name']

    def _get_moto_type(self, moto_number):
        return self.response['offers'][moto_number]['vehicle_info']['moto_type']

    def _get_displacement(self, moto_number):
        return self.response['offers'][moto_number]['vehicle_info']['displacement']

    def _get_color(self, moto_number):
        color_hex = self.response['offers'][moto_number]['color_hex']
        return color_hex

    def _get_transmission(self, moto_number):
        return self.response['offers'][moto_number]['vehicle_info']['transmission']

    def _get_saleId(self, moto_number):
        return self.response['offers'][moto_number]['saleId']

    def _get_link(self, moto_number):
        mark_info = self._get_mark_info(moto_number)
        model_code = self.response['offers'][moto_number]['vehicle_info']['model_info']['code']
        saleId = self._get_saleId(moto_number)
        return f'https://auto.ru/motorcycle/used/sale/{mark_info}/{model_code}/{saleId}/'

    def _get_price(self, moto_number):
        return self.response['offers'][moto_number]['price_info']['RUR']

    def _get_mileage(self, moto_number):
        return self.response['offers'][moto_number]['state']['mileage']

    def _get_horse_power(self, moto_number):
        return self.response['offers'][moto_number]['vehicle_info']['horse_power']

    def _get_comments(self, moto_number):
        link = self._get_link(moto_number)
        r = requests.get(link, headers=self.headers, cookies=self.cookies)
        tree = html.fromstring(r.content)
        descriptions_xpath = tree.xpath(
            '//*[@id="app"]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[7]/div/div/div//text()')
        return descriptions_xpath

    def _get_list_images_small(self, moto_number):
        image_list_thumb = []
        images_count = self.response['offers'][moto_number]['state']['images_count']
        count = images_count if images_count < 10 else 10  # it's getting max 10 images from api on main page
        for img_number in range(count):
            image_list_thumb.append(
                self.response['offers'][moto_number]['state']['image_urls'][img_number]['sizes']['320x240'])
        return image_list_thumb

    def _get_list_images_large(self, moto_number):
        image_list_large = []
        images_count = self.response['offers'][moto_number]['state']['images_count']
        count = images_count if images_count < 10 else 10  # it's getting max 10 images from api on main page
        for img_number in range(count):
            image_list_large.append(
                self.response['offers'][moto_number]['state']['image_urls'][img_number]['sizes']['1200x900'])
        return image_list_large

    def _get_region(self, moto_number):
        return self.response['offers'][moto_number]['seller']['location']['region_info']['name']

    @staticmethod
    def _save_image_and_return_path(motorcycle_id, n, image_link):
        img_path_save = f"media/images/{motorcycle_id}/{image_link.split('/')[-1]}_{n}.png"
        try:
            os.makedirs(f"media/images/{motorcycle_id}/")
        except OSError as err:
            pass
        image_link = 'https://' + image_link.split('//')[1]
        r = requests.get(image_link)
        with open(img_path_save, 'wb') as img:
            img.write(r.content)
        return img_path_save.replace('media/', '')

    def fill_db(self):
        total_info = self._get_total_info()
        # pages = total_info['total_page_count']

        pages = 1
        # moving on pages
        for page in range(1, pages + 1):
            self.json_data['page'] = page
            self._get_new_requests_post()
            # total_offers_on_page = total_info['total_offers_on_page']
            total_offers_on_page = 10

            # moving on offers
            for moto_number in tqdm(range(total_offers_on_page), f'Page: {page}'):
                try:
                    mark_info = self._get_mark_info(moto_number)
                    if mark_info not in [mark.name for mark in Marks.objects.all()]:
                        mark_info = Marks.objects.create(name=mark_info)
                    else:
                        mark_info = Marks.objects.get(name=mark_info)

                    model_info = self._get_model_info(moto_number)
                    if model_info not in [model.name for model in Moto_models.objects.all()]:
                        model_info = Moto_models.objects.create(name=model_info)
                    else:
                        model_info = Moto_models.objects.get(name=model_info)

                    type_moto = self._get_moto_type(moto_number)
                    if type_moto not in [moto_type.name for moto_type in Moto_type.objects.all()]:
                        type_moto = Moto_type.objects.create(name=type_moto)
                    else:
                        type_moto = Moto_type.objects.get(name=type_moto)

                    displacement = self._get_displacement(moto_number)
                    if displacement not in [disp.number for disp in Displacement.objects.all()]:
                        displacement = Displacement.objects.create(number=displacement)
                    else:
                        displacement = Displacement.objects.get(number=displacement)

                    color_hex = self._get_color(moto_number)
                    color_r = requests.get(f'https://www.thecolorapi.com/id?hex={color_hex}').json()
                    color_name = color_r['name']['value']
                    color_hex = '#' + color_hex
                    if color_hex not in [color.color_hex for color in Color.objects.all()]:
                        color = Color.objects.create(name=color_name, color_hex=color_hex)
                    else:
                        color = Color.objects.get(color_hex=color_hex)

                    transmission = self._get_transmission(moto_number)
                    if transmission not in [transmissions.name for transmissions in Transmission.objects.all()]:
                        transmission = Transmission.objects.create(name=transmission)
                    else:
                        transmission = Transmission.objects.get(name=transmission)

                    city_name = self._get_region(moto_number)
                    if city_name not in [city.name for city in City.objects.all()]:
                        city = City.objects.create(name=city_name)
                    else:
                        city = City.objects.get(name=city_name)

                    mileage = self._get_mileage(moto_number)
                    horse_power = self._get_horse_power(moto_number)
                    price = self._get_price(moto_number)
                    comment = self._get_comments(moto_number)
                except KeyError as err:
                    print(f'\nERROR({page}, {moto_number}): \n', err)
                    continue

                current_motocycle = Motorcycle.objects.create(
                    mark_info=mark_info,
                    model_info=model_info,
                    moto_type=type_moto,
                    displacement=displacement,
                    city=city,
                    color=color,
                    mileage=mileage,
                    horse_power=horse_power,
                    price=price,
                    transmission=transmission,
                    comment=comment,
                    user=StoreAppUser.objects.get(pk=1)
                )

                # images processing block
                # small images
                # list_small_images = self._get_list_images_small(moto_number)
                # for image_id, img_link in enumerate(list_small_images, 0):
                #     img_path = self._save_image_and_return_path(current_motocycle.id,
                #                                                 n=image_id,
                #                                                 image_link=img_link)
                #     Motorcycle_images.objects.create(image=img_path, moto=current_motocycle)
                # large images
                list_large_images = self._get_list_images_large(moto_number)
                for image_id, img_link in enumerate(list_large_images, 0):
                    img_path = self._save_image_and_return_path(current_motocycle.id,
                                                                n=image_id,
                                                                image_link=img_link)
                    Motorcycle_images.objects.create(image=img_path, moto=current_motocycle)
