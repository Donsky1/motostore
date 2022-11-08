# Motorcycle Store
<p><img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/logo.png'></p>
<h2>Website Using Django</h2>

Навигация по документации:
<ul>
  <li><a href='#overview'>Обзор</a></li>
  <li><a href='#structure'>Структура сайта Motorcycle Store</a></li>
  <li><a href='#feature'>Особенность</a></li>
  <li><a href='#installation'>Установка</a></li>
  <li><a href='#telegram'>Telegram Bot</a></li>
  <li><a href='#api'>API</a></li>
    <ul>
      <li><a href='#curl_api_read'>API read</a></li>
      <li><a href='#curl_api_write'>API write</a></li>
    </ul>
</ul>

<h2 id='overview'>Обзор</h2>
<p><b>Motorcycle Store</b> - интернет площадка  для размещения объявлений для юр и физ лиц посвященная продаже "мотоциклов".</p>
<p>Данный сайт представляет из себя упрощенную версию классифайд площадки -  ресурса с объявлениями от физических и юридических лиц с различными предложениями, широко известных на просторах рунета <b>auto.ru</b> или <b>avito.ru</b>. Однако тут тематика узкоспециализированная, и это мотоциклы.</p>

<br>
<p><img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/readme/main_page.png' align="center"></p>
<br>
<p>
<img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/favicon.png' width=300px align="right">
<b id='structure'>Структура сайта</b>:
<ol>
  <li>Главная</li>
  <ul>
    <li>Торговая площадка - отображаются все активные объявления</li>
    <li>Разместить объявление</li>
  </ul>
  <li>Новости</li>
  <ul>
    <li>Публикации - новостной раздел сайта</li>
    <li>Опубликовать новость</li>
  </ul>
  <li>Проект</li>
    <ul>
      <li>О проекте - информация о сайте</li>
      <li>Контакты - форма обратной связи</li>
    </ul>
  <li>Условия - техническая информация, лицензия</li>
  <li>Профиль</li>
    <ul>
      <li>"Пользователь" - страница с профилем пользователя</li>
      <li>Выход</li>
    </ul>
</ol>
</p>

<br>
<p id='feature'><b>Особенность</b></p>
<img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/readme/telegram_offer.png' width=320px align="right">
<ul>
  <li>Парсер объявлений для заполнения БД с сайта auto.ru. (<i>Инструкция будет ниже</i>)</li>
  <li>Система авторизации пользователей</li>
  <li>Пагинация на веб странице</li>
  <li>Права доступа</li>
  <li>API</li>
  <li>Telegram Bot. Запросы пользователй и информация о пользователях сохраняется в БД для дальнейшего анализа.(<i>Инструкция будет ниже</i>)</li>
  <li>Пагинация в телеграм боте</li>
  <li>Если в профиле пользователь укажет свой телеграм аккаунт или телефон, то имеется способ напрямую связаться с ним через телеграм объявление</li>
  <li>Объявления и новости могут публиковать только авторизованные пользователи. Новости могут публиковать только пользователи со статусом author</li>
  <li>Редактирование новостей и объявлений возможна, как на главной странице, так и на странице профиля пользователей и в самой новости или объявлении. Пользователь может редактировать, удалять только свои.</li>
  <li>На странице профиля можно увидеть все объявления и новости с указанием количества.</li>
  <li>На странице профиля можно изменить токен для api доступа без перезарузки страницы на ajax, информацию профиля, пароль</li>
  <li>Имеется два блока поиска по ключевым словам</li>
  <li>Имеется динамический блок фильтрации контекта по марке, модели, типу мотоцикла, а также цены без перезарузки страницы на ajax </li>
  <li>Имеется блок типов мотоцикла для ускоренной фильтрации контента</li>
  <li>Имеется блок часто просматриваемых объявлений</li>
</ul>
<br>
<img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/readme/motorcycle.png'>
<br>
<br>
<h2 id='installation'>Установка (действия будут выполнятся на windows)</h2>
<p>1. Создаем директорию, клонируем проект в эту папку ... <p>

```
git clone ..
```
<p>2. Переходим в папку с проектом, выполнив команду cd <p>

```
cd motostore/motostore
```
<p>3. Установим все необходимые библиотеки, используя pip ... <p>
  
```pip
pip install -r requirements.txt
```
<p>4. Создадим новые миграции<p>

  ```
manage.py makemigrations 
```
<p>5. Применим миграции <p>

  ```
manage.py migrate  
```
<p>5.1 Создадим суперпользователя. Он нам понадобиться для парсинга. Именно на него будут заводиться все объявления<p>

  ```
manage.py createsuperuser
```
<h2>Парсинг объявлений с сайта auto.ru (в рамках обучения)</h2>
<p>6. На данный момент все готово, но данных пока у нас нет, поэтому выполним парсинг с сайта auto.ru. Т.к сайт динамически обновляет контент, необходимо ...<p>
<p>6.1. Создаем config.py в директории storeapp/management/, т.е  должно получиться storeapp/management/config.py<p>
<p>6.2. Заходим на сайт в раздел мотоциклы [auto.ru](https://auto.ru/motorcycle/all/). Открываем инструменты разработчика Ctrl+Shift+I или F12<p>
<img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/readme/auto1.png' width=300px>
<p>6.3. Далее следуем инструкциям по картинке: <p>
<img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/readme/auto2.png' width=300px>
<img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/readme/auto3.png' width=300px>
<img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/readme/auto4.png' width=300px>
<p>6.4. Скопированный cURL  вставляем в любой cURL конвертер онлайн<p>
<img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/readme/auto5.png' width=300px>
<p>6.5. Получаем request запрос на языке python. (да там много языков, нам нужен python). Копируем словари cookies и headers в ранее созданный файл config.py.<p>
<p>6.6. (Опционально) Словарь json_data можем изменить в файле fillstore,  именно в нем задаются параметры запроса. В целом достаточно изменять ключ "catalog_filter" в json_data. Параметры опять же можно узнать в раскодированной curl соманде <p>
<p>6.7. Выполняем парсинг любой командой (-w --wait задает время ожидания между запросами, если не задано, то случайное число в диапазоне от 10 до 35 сек.): <p> 

```
manage.py fillstore
manage.py fillstore -w 30
manage.py fillstore --wait 30
```
<p>6.8. Запускаем сервер командой<p>
  
```
manage.py runserver
```
<p>7. При попытке зайти на сайт мы увидим, что сайт будет пустым. Это связано с тем, что объявления которые спарсились находятся в неактивном статусе, т.е. их нужно активировать. Для этого заходим в админку: wedsite/admin. Логинимся под суперпользователем, которого создали в пунке 5.1. Далее в раздел мотоциклы, все выделяем галочкой и выполняем команду: "Опубликовать"<p>
<p>8. Снова заходим на сайт.<p>
<p> Можно увидеть, что некоторые пункты меню недоступны для неавторизованных пользователей. Новостной раздел пока пустой, но можно смело зайти и создать их.<p>

<br>
<h2 id='telegram'>Запуск телеграм бота в синхронизации с сайтом</h2>
<i>Далее инструкция представлена из расчета, что пользователь уже знает, как создать пустого бота в телеграм, получить token</i><br><br>

<p>1. Создаем файл telegram_config по следующей директории: telegramapp.management.<b>telegram_config</b><p>
<p>2. Создаем в файле telegram_config константы TOKEN, PATH_TO_IMAGES</b><p>

```
TOKEN = 'TelegramBotToken'
PATH_TO_IMAGES = 'absolute path to motostore' # к примеру C:/../../motostore
```
<p>3. Запускам бота командой <p>
  
```
manage.py telegram
```
<p>4. Открываем своего бота и вводим команду<p>
   
```
/start
```
 
<br>
<h2 id='api'>API</h2>
<p>API функционал выполнен с использованием Django REST framework</p>
<p>Неавторизованные пользователи получают доступ только на чтение, а вот авторизованные могут выполнять действия в зависимости от прав доступа. На проекте доступны 3 вида аутентификации: базовый на основе пароля и логина, сессии и токен аутентификация</p>

```
'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
 ...
'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
```
<p>API Root запрос выполняется на <b>website/api/v0/</b><p>

```
/api/v0/
```
<p>Остальные API запросы выполняется на <b>website/api/v0/request</b><p>

```
mark list: /api/v0/marks/
models: /api/v0/motorcycle-models/
news: /api/v0/news/
...
```
<p id='curl_api_read'>сURL API запрос на чтение</p> 

```
curl -X GET http://website/api/v0/
  
```
<p id='curl_api_write'>сURL API запрос на запись</p> 

```
curl -X GET http://website/api/v0/
  
```
