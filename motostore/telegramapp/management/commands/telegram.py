import telebot
import requests
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
from django.db.models import Q

from telegramapp.management.telegram_config import TOKEN, PATH_TO_IMAGES
from storeapp.models import Motorcycle


MAIN_URL = 'http://127.0.0.1:8000'
API_REQUEST = '/api/v0'


class MyStates(StatesGroup):
    type_motorcycle = State()
    mark_motorcycle = State()
    model_motorcycle = State()
    displacement_motorcycle = State()


state_storage = StateMemoryStorage()

bot = telebot.TeleBot(TOKEN, state_storage=state_storage)


def FILTER_MOTORCYCLES(filter_str: str):
    print(f'Сработал запрос к апи для полученния {filter_str} мотоцикла')
    response = requests.get(f'{MAIN_URL}{API_REQUEST}/{filter_str}/').json()
    return [el['name'] for el in response['results']]


TYPES_MOTORCYCLE = FILTER_MOTORCYCLES('motorcycle-types')
MARKS_MOTORCYCLE = FILTER_MOTORCYCLES('marks')
MODELS_MOTORCYCLE = FILTER_MOTORCYCLES('motorcycle-models') + ['All models']


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
    request_state_type = request_state.split(',')[0]
    request_state_mark = request_state.split(',')[1]
    queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type').filter(
        moto_type__name=request_state_type,
        mark_info__name=request_state_mark)
    model_motorcycles = {motorcycle.model_info.name for motorcycle in queryset}
    return telebot.types.InlineKeyboardMarkup(
        keyboard=[
            [
                telebot.types.InlineKeyboardButton(model, callback_data=f'{request_state},{model}')
            ] for model in model_motorcycles
        ]
    )


def displacement_motorcycle(request_state):
    request_state_type = request_state.split(',')[0]
    request_state_mark = request_state.split(',')[1]
    queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type').filter(
        moto_type__name=request_state_type,
        mark_info__name=request_state_mark)
    displacement_motorcycles = {motorcycle.displacement.number for motorcycle in queryset}
    markup = telebot.types.InlineKeyboardMarkup()
    btn_buttons = list()
    for disp in displacement_motorcycles:
        if 0 <= disp <= 250:
            btn_buttons.append(telebot.types.InlineKeyboardButton('<250', callback_data=f'{request_state},250'))
        if 251 <= disp <= 400:
            btn_buttons.append(telebot.types.InlineKeyboardButton('251-400', callback_data=f'{request_state},251 400'))
        if 401 <= disp <= 600:
            btn_buttons.append(telebot.types.InlineKeyboardButton('401-600', callback_data=f'{request_state},401 600'))
        if 601 <= disp <= 800:
            btn_buttons.append(telebot.types.InlineKeyboardButton('601-800', callback_data=f'{request_state},601 800'))
        if 801 <= disp <= 2000:
            btn_buttons.append(telebot.types.InlineKeyboardButton('801>', callback_data=f'{request_state},801'))
    btn_buttons = set(btn_buttons)
    markup.row(*btn_buttons)
    return markup


def menu_btn():
    return telebot.types.InlineKeyboardMarkup(
        [
            [
                telebot.types.InlineKeyboardButton('Вперед', callback_data='next_page'),
                telebot.types.InlineKeyboardButton('1 из 100', callback_data='page'),
                telebot.types.InlineKeyboardButton('Назад', callback_data='back_page'),
            ]
        ]
    )


def get_displacement(call):
    # print(call.data)
    return True


def get_result_motorcycles(moto_type, mark_info, model_info, displacement: list):
    if model_info != 'All models':
        if len(displacement) == 1 and displacement[0] == 250:
            queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type', 'displacement'). \
                filter(Q(moto_type__name=moto_type),
                       Q(mark_info__name=mark_info),
                       Q(model_info__name=model_info),
                       Q(displacement__number__gte=0) | Q(displacement__number__lte=250))
        elif len(displacement) == 1 and displacement[0] == 801:
            queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type', 'displacement'). \
                filter(Q(moto_type__name=moto_type),
                       Q(mark_info__name=mark_info),
                       Q(model_info__name=model_info),
                       Q(displacement__number__gte=801))
        else:
            gte = displacement[0]
            lte = displacement[1]
            queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type', 'displacement').filter(Q(moto_type__name=moto_type),
                       Q(mark_info__name=mark_info),
                       Q(model_info__name=model_info),
                       Q(displacement__number__gte=gte) | Q(displacement__number__lte=lte))
    else:
        if len(displacement) == 1 and displacement[0] == 250:
            queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type', 'displacement'). \
                filter(Q(moto_type__name=moto_type),
                       Q(mark_info__name=mark_info),
                       Q(displacement__number__gte=0) | Q(displacement__number__lte=250))
        elif len(displacement) == 1 and displacement[0] == 801:
            queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type', 'displacement'). \
                filter(Q(moto_type__name=moto_type),
                       Q(mark_info__name=mark_info),
                       Q(displacement__number__gte=801))
        else:
            gte = displacement[0]
            lte = displacement[1]
            queryset = Motorcycle.active_offer.select_related('mark_info', 'model_info', 'moto_type', 'displacement'). \
                filter(Q(moto_type__name=moto_type),
                       Q(mark_info__name=mark_info),
                       Q(displacement__number__gte=gte) | Q(displacement__number__lte=lte))
    return queryset



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
    model_motorcycle_markup = model_motorcycle(request_state=call.data)
    model_motorcycle_markup.row(
        telebot.types.InlineKeyboardButton('All models', callback_data='All models')
    )
    bot.edit_message_text(chat_id=call.message.chat.id,
                          text='Выберите модель мотоцикла',
                          message_id=call.message.id,
                          reply_markup=model_motorcycle_markup)


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
    bot.edit_message_text(chat_id=call.message.chat.id,
                          text='Результат',
                          message_id=call.message.id,
                          reply_markup=result)


@bot.callback_query_handler(func=lambda call: 'result' in call.data)
def callback_query_result(call):
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        try:
            displacement = [int(disp) for disp in data.get('displacement_motorcycle').split(' ')]
        except Exception:
            displacement = [int(data.get('displacement_motorcycle'))]

        queryset = get_result_motorcycles(moto_type=data.get('type_motorcycle'),
                                          mark_info=data.get('mark_motorcycle'),
                                          model_info=data.get('model_motorcycle'),
                                          displacement=displacement)
        for motorcycle in queryset:
            msg = f"<b>{motorcycle.mark_info} {motorcycle.model_info}</b>\n\n" \
                  f"Город: {motorcycle.city}\n" \
                  f"Рейтинг просмотров: {motorcycle.rate}\n\n" \
                  f"Тип: {motorcycle.moto_type}\n" \
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
                  f"Телефон: {motorcycle.user.phone}\n" \
                  f"Написать в телеграмм: <i>(в разработке)</i>\n"\
                  f"Ссылка на объявление: {MAIN_URL}/motorcycle/{motorcycle.id}"
            with open(PATH_TO_IMAGES + f'{motorcycle.motorcycle_images_set.first().image.url}', 'rb') as image:
                bot.send_photo(call.message.chat.id, image, caption=msg, parse_mode='html', reply_markup=menu_btn())
    bot.delete_state(call.from_user.id, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'back_page')
def back(call):
    pass


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.infinity_polling(skip_pending=True)
