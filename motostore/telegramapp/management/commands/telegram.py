import telebot
import requests
import json
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
from django.db.models import Q
from uuid import uuid4

from telegramapp.management.telegram_config import TOKEN, PATH_TO_IMAGES
from storeapp.models import Motorcycle
from telegramapp.models import TelegramRequest, TelegramUser

MAIN_URL = 'http://127.0.0.1:8000'
API_REQUEST = '/api/v0'


class MyStates(StatesGroup):
    type_motorcycle = State()
    mark_motorcycle = State()
    model_motorcycle = State()
    displacement_motorcycle = State()


state_storage = StateMemoryStorage()

bot = telebot.TeleBot(TOKEN, state_storage=state_storage)


def FILTER_MOTORCYCLES(filter_str: str, field: str = 'name'):
    print(f'Сработал запрос по апи для полученния {filter_str} мотоцикла')
    page = 1
    temp_list = []
    while True:
        response = requests.get(f'{MAIN_URL}{API_REQUEST}/{filter_str}/?page={page}').json()
        for el in response['results']:
            temp_list.append(el[field])
        if response['next']:
            page += 1
        else:
            return temp_list


TYPES_MOTORCYCLE = FILTER_MOTORCYCLES('motorcycle-types')
MARKS_MOTORCYCLE = FILTER_MOTORCYCLES('marks')
MODELS_MOTORCYCLE = FILTER_MOTORCYCLES('motorcycle-models')


def btn_open_web():
    return telebot.types.InlineKeyboardMarkup(
        keyboard=[
            [
                telebot.types.InlineKeyboardButton('Motorcycle Store', url=MAIN_URL)
            ]
        ]
    )


def type_motorcycle():
    response = requests.get(f'{MAIN_URL}{API_REQUEST}/motorcycle-types/').json()
    type_motorcycles = response['results']
    return telebot.types.InlineKeyboardMarkup(
        keyboard=[
            [
                telebot.types.InlineKeyboardButton(type_m['name'], callback_data=type_m['name'])
            ] for type_m in type_motorcycles
        ]
    )


def mark_motorcycle(request_state):
    queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type', ).filter(
        moto_type__name=request_state)
    mark_motorcycles = {motorcycle.mark_info.name for motorcycle in queryset}
    return telebot.types.InlineKeyboardMarkup(
        keyboard=[
            [
                telebot.types.InlineKeyboardButton(mark, callback_data=f'{request_state},{mark}')
            ] for mark in mark_motorcycles
        ]
    )


def model_motorcycle(request_state):
    request = request_state.split(',')
    request_state_type = request[0]
    request_state_mark = request[1]
    request_state_displacement = request[2]

    try:
        displacement = request_state_displacement.split(' ')
        gte = int(displacement[0])
        lte = int(displacement[1])
    except Exception:
        gte = 0
        lte = int(request_state_displacement)

    queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type').filter(
        Q(moto_type__name=request_state_type),
        Q(mark_info__name=request_state_mark),
        Q(displacement__number__gte=gte) & Q(displacement__number__lte=lte))
    model_motorcycles = {motorcycle.model_info.name for motorcycle in queryset}
    return telebot.types.InlineKeyboardMarkup(
        keyboard=[
            [
                telebot.types.InlineKeyboardButton(model, callback_data=f'{request_state},{model}')
            ] for model in model_motorcycles
        ]
    )


def displacement_motorcycle(request_state):
    displacement_dict = {
        1: telebot.types.InlineKeyboardButton('< 250', callback_data=f'{request_state},0 250'),
        2: telebot.types.InlineKeyboardButton('251-400', callback_data=f'{request_state},251 400'),
        3: telebot.types.InlineKeyboardButton('401-600', callback_data=f'{request_state},401 600'),
        4: telebot.types.InlineKeyboardButton('601-800', callback_data=f'{request_state},601 800'),
        5: telebot.types.InlineKeyboardButton('801 >', callback_data=f'{request_state},801 2000'),
    }
    request_state_type = request_state.split(',')[0]
    request_state_mark = request_state.split(',')[1]
    queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type').filter(
        moto_type__name=request_state_type,
        mark_info__name=request_state_mark)
    displacement_motorcycles = {motorcycle.displacement.number for motorcycle in queryset}
    markup = telebot.types.InlineKeyboardMarkup()
    btn_buttons = list()
    btn_buttons_InlineKeyboards = list()
    for disp in displacement_motorcycles:
        if 0 <= disp <= 250:
            btn_buttons.append(1)
        if 251 <= disp <= 400:
            btn_buttons.append(2)
        if 401 <= disp <= 600:
            btn_buttons.append(3)
        if 601 <= disp <= 800:
            btn_buttons.append(4)
        if 801 <= disp <= 2000:
            btn_buttons.append(5)
    for i in set(btn_buttons):
        btn_buttons_InlineKeyboards.append(displacement_dict[i])
    markup.row(*btn_buttons_InlineKeyboards)
    return markup


def get_displacement(call):
    return True


def get_result_motorcycles(moto_type, mark_info, model_info, displacement: list) -> list:
    gte = displacement[0]
    lte = displacement[1]
    queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type', 'displacement'). \
        filter(Q(moto_type__name=moto_type),
               Q(mark_info__name=mark_info),
               Q(model_info__name=model_info),
               Q(displacement__number__gte=gte) & Q(displacement__number__lte=lte))
    return [motorcycle.id for motorcycle in queryset]


def last_menu_btn(state):
    json_string = json.loads(state)
    curr_id = json_string['id']
    uuid = json_string['uuid']
    current_request = TelegramRequest.objects.get(uuid=uuid)
    print(json_string)
    print(current_request)
    # '[1, 2]' -> ['1', '2']
    results = current_request.motorcycle_ids.replace('[', '').replace(']', '').split(', ')
    count = len(results)
    first_id = int(results[0])
    last_id = int(results[-1])
    page = results.index(str(curr_id)) + 1
    print(curr_id, first_id, last_id)
    if count == 1:
        return telebot.types.InlineKeyboardMarkup(
            [
                [
                    telebot.types.InlineKeyboardButton(f'{page} из {count}', callback_data='#'),
                ]
            ]
        )
    if count > 1 and curr_id == first_id:
        print('count > 1 and curr_id == first_id')
        return telebot.types.InlineKeyboardMarkup(
            [
                [
                    telebot.types.InlineKeyboardButton('Вперед', callback_data='{\"id\":' + str(
                        results[results.index(str(curr_id)) + 1]) + f',\"uuid\":\"{uuid}\"' + '}'),
                    telebot.types.InlineKeyboardButton(f'{page} из {count}', callback_data='#'),
                ]
            ]
        )
    elif count > 1 and curr_id == last_id:
        print('count > 1 and id == last_id')
        return telebot.types.InlineKeyboardMarkup(
            [
                [
                    telebot.types.InlineKeyboardButton(f'{page} из {count}', callback_data='#'),
                    telebot.types.InlineKeyboardButton('Назад', callback_data='{\"id\":' + str(
                        results[results.index(str(curr_id)) - 1]) + f',\"uuid\":\"{uuid}\"' + '}'),
                ]
            ]
        )
    else:
        print('else block')
        return telebot.types.InlineKeyboardMarkup(
            [
                [
                    telebot.types.InlineKeyboardButton('Вперед', callback_data='{\"id\":' + str(
                        results[results.index(str(curr_id)) + 1]) + f',\"uuid\":\"{uuid}\"' + '}'),
                    telebot.types.InlineKeyboardButton(f'{page} из {count}', callback_data='#'),
                    telebot.types.InlineKeyboardButton('Назад', callback_data='{\"id\":' + str(
                        results[results.index(str(curr_id)) - 1]) + f',\"uuid\":\"{uuid}\"' + '}'),
                ]
            ]
        )


def _get_motorcycle_offer(motorcycle):
    if motorcycle.user.telegram_account:
        telegram_account = f"Написать в телеграмм: <a href='https://t.me/{motorcycle.user.telegram_account}'>{motorcycle.user.telegram_account}</a>\n"
    else:
        telegram_account = ''

    return f"<b>{motorcycle.mark_info} {motorcycle.model_info}</b>\n\n" \
           f"Город: {motorcycle.city}\n" \
           f"Рейтинг просмотров: {motorcycle.rate}\n\n" \
           f"Тип: {motorcycle.moto_type.translate}\n" \
           f"Объем дигателя: {motorcycle.displacement} см³\n" \
           f"Пробег: {motorcycle.mileage} км\n" \
           f"Мощность {motorcycle.horse_power} л.с\n" \
           f"Кол-во передач: {str(motorcycle.transmission).split('_')[-1]}\n" \
           f"Цвет мотоцикла: {motorcycle.color}\n\n" \
           f"Комметарий продавца: \n" \
           f"{motorcycle.comment[:100]} ...\n" \
           f"\n" \
           f"Цена: <b>{motorcycle.price}</b> руб.\n\n" \
           f"<u>Контакты:</u>\n" \
           f"Пользователь: {motorcycle.user.username}\n" \
           f"Телефон: {motorcycle.user.phone}\n" + telegram_account + \
           f"Ссылка на объявление: <a href='{MAIN_URL}/motorcycle/{motorcycle.id}'>ссылка</a>"


def _get_or_create_telegram_user(call):
    telegram_id = call.from_user.id

    user, created = TelegramUser.objects.get_or_create(telegram_id=telegram_id)
    if created:
        user.first_name = call.from_user.first_name if call.from_user.first_name else ''
        user.username = call.from_user.username if call.from_user.username else ''
        user.last_name = call.from_user.last_name if call.from_user.last_name else ''
        user.language_code = call.from_user.language_code if call.from_user.language_code else ''
        user.save()
    return user


@bot.message_handler(commands=['start'])
def get_menu(message):
    menu = telebot.types.ReplyKeyboardMarkup(True, True)
    menu.row('Открыть сайт в браузере')
    menu.row('Выбор мотоцикла')
    bot.send_message(message.chat.id, 'Что выберешь?', reply_markup=menu)


@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text == 'Открыть сайт в браузере':
        bot.send_message(message.chat.id, MAIN_URL, reply_markup=btn_open_web())

    if message.text == 'Выбор мотоцикла':
        bot.set_state(message.from_user.id, MyStates.type_motorcycle, message.chat.id)
        bot.send_message(message.chat.id, 'Выберите тип мотоцикла', reply_markup=type_motorcycle())


@bot.callback_query_handler(func=lambda call: call.data in TYPES_MOTORCYCLE, state=MyStates.type_motorcycle)
def callback_query_type(call):
    print('сработал call type')
    bot.set_state(call.from_user.id, MyStates.mark_motorcycle, call.message.chat.id)
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        data['type_motorcycle'] = call.data
    bot.edit_message_text(chat_id=call.message.chat.id,
                          text='Выберите марку мотоцикла',
                          message_id=call.message.id,
                          reply_markup=mark_motorcycle(request_state=call.data))


@bot.callback_query_handler(func=lambda call: call.data.split(',')[-1] in MARKS_MOTORCYCLE,
                            state=MyStates.mark_motorcycle)
def callback_query_mark(call):
    print('сработал call mark')
    bot.set_state(call.from_user.id, MyStates.displacement_motorcycle, call.message.chat.id)
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        data['mark_motorcycle'] = call.data.split(',')[-1]
    bot.edit_message_text(chat_id=call.message.chat.id,
                          text='Выберите объем двигателя',
                          message_id=call.message.id,
                          reply_markup=displacement_motorcycle(request_state=call.data))


@bot.callback_query_handler(func=get_displacement,
                            state=MyStates.displacement_motorcycle)
def callback_query_displacement(call):
    print('сработал call displacement')
    bot.set_state(call.from_user.id, MyStates.model_motorcycle, call.message.chat.id)
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        data['displacement_motorcycle'] = call.data.split(',')[-1]
    bot.edit_message_text(chat_id=call.message.chat.id,
                          text='Выберите модель мотоцикла',
                          message_id=call.message.id,
                          reply_markup=model_motorcycle(request_state=call.data))


@bot.callback_query_handler(func=lambda call: call.data.split(',')[-1] in MODELS_MOTORCYCLE,
                            state=MyStates.model_motorcycle)
def callback_query_model(call):
    print('сработал call model')
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        data['model_motorcycle'] = call.data.split(',')[-1]
    result = telebot.types.InlineKeyboardMarkup(
        keyboard=[
            [telebot.types.InlineKeyboardButton('Получить результат', callback_data='result')],
        ]
    )
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        msg = f"Вы выбрали: \n" \
              f"Тип мотоцикла: {data.get('type_motorcycle')}\n" \
              f"Марка: {data.get('mark_motorcycle')} \n" \
              f"Модель: {data.get('model_motorcycle')}\n"

    bot.edit_message_text(chat_id=call.message.chat.id,
                          text=msg,
                          message_id=call.message.id,
                          reply_markup=result)


@bot.callback_query_handler(func=lambda call: 'result' in call.data)
def callback_query_result(call):
    if call.data == 'result':
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            displacement = [int(disp) for disp in data.get('displacement_motorcycle').split(' ')]

            ids_list = get_result_motorcycles(moto_type=data.get('type_motorcycle'),
                                              mark_info=data.get('mark_motorcycle'),
                                              model_info=data.get('model_motorcycle'),
                                              displacement=displacement)
            uuid = str(uuid4())
            user = _get_or_create_telegram_user(call)
            TelegramRequest.objects.create(chat_id=call.message.chat.id,
                                           uuid=uuid,
                                           user=user,
                                           motorcycle_ids=ids_list)

            motorcycle = Motorcycle.active_offer.get(pk=ids_list[0])
            msg = _get_motorcycle_offer(motorcycle)
            with open(PATH_TO_IMAGES + f'{motorcycle.motorcycle_images_set.first().image.url}', 'rb') as image:
                bot.send_photo(call.message.chat.id, image, caption=msg, parse_mode='html',
                               reply_markup=last_menu_btn(
                                   state='{\"id\":' + str(motorcycle.id) + f',\"uuid\":\"{uuid}\"' + '}'))
        bot.delete_state(call.from_user.id, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: 'id' in call.data)
def callback_query_result(call):
    json_string = json.loads(call.data)
    pk = json_string['id']
    uuid = json_string['uuid']
    print('-'*20)
    print('2Page: ', pk, uuid)
    motorcycle = Motorcycle.active_offer.get(id=pk)
    msg = _get_motorcycle_offer(motorcycle)
    with open(PATH_TO_IMAGES + f'{motorcycle.motorcycle_images_set.first().image.url}', 'rb') as image:
        bot.send_photo(call.message.chat.id, image, caption=msg, parse_mode='html',
                       reply_markup=last_menu_btn(
                           state='{\"id\":' + str(motorcycle.id) + f',\"uuid\":\"{uuid}\"' + '}'))


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.infinity_polling(skip_pending=True)
