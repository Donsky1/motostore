# Motorcycle Store
<p><img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/logo.png'></p>
<h3>Website Using Django</h3>

<h2>Обзор</h2>
<p><b>Motorcycle Store</b> - интернет площадка  для размещения объявлений для юр и физ лиц посвященная продаже "мотоциклов".</p>
<p>Данный сайт представляет из себя упрощенную версию классифайд площадки -  ресурса с объявлениями от физических и юридических лиц с различными предложениями, широко известных на просторах рунета <b>auto.ru</b> или <b>avito.ru</b>. Однако тут тематика узкоспециализированная, и это мотоциклы.</p>

<br>
<p><img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/readme/main_page.png' align="center"></p>
<br>
<p>
<img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/favicon.png' width=300px align="right">
<b>Структура сайта</b>:
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
<p><b>Функционал</b></p>
<img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/readme/telegram_offer.png' width=320px align="right">
<ul>
  <li>Парсер объявлений для заполнения БД с сайта auto.ru. (<i>Инструкция будет ниже</i>)</li>
  <li>Система авторизации пользователей</li>
  <li>Пагинация на веб странице</li>
  <li>Права доступа</li>
  <li>API</li>
  <li>Telegram Bot</li>
  <li>Пагинация в телеграм боте</li>
  <li>Если в профиле пользователь укажет свой телеграм аккаунт или телефон, то имеется способ напрямую связаться с ним через телеграм объявление</li>
  <li>Объявления и новости могут публиковать только авторизованные пользователи. Новости могут публиковать только пользователи со статусом author</li>
  <li>Редактирование новостей и объявлений возможна, как на главной странице, так и на странице профиля пользовтеля и в самой новости или объявлении. Пользователь может редактировать, удалять только свои.</li>
  <li>На странице профиля можно увидеть все объявления и новости с указанием количества.</li>
  <li>На странице профиля можно изменить токен для api доступа без перезарузки страницы на ajax, информацию профиля, пароль</li>
  <li>Имеется два блока поиска по ключевым словам</li>
  <li>Имеется динамический блок фильтрации контекта по марке, модели, типу мотоцикла, а также цене без перезарузки страницы на ajax </li>
  <li>Имеется блок типов мотоцикла для ускоренной фильтрации контента</li>
  <li>Имеется блок часто просматриваемых объявлений</li>
</ul>
<br>
<img src='https://github.com/Donsky1/motostore/blob/main/motostore/static/images/readme/motorcycle.png'>
<br>
<br>
<h2>Установка (действия будут выполнятся на windows)</h2>
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
<p>6.5. Выполняем парсинг любой командой (-w --wait задает время ожидания между запросами, если не задано, то случайное число в диапазоне от 10 до 35 сек.): <p> 

```
manage.py fillstore
manage.py fillstore -w 30
manage.py fillstore --wait 30
```
<p>6.6. Запускаем сервер <p>
```
manage.py runserver
```
<p>7. При попытке зайти сайт будет пустым, это связано с тем, что объявления которые спарсились находятся в неактивном статусе, т.е. их нужно активировать. Для этого заходим в админку: wedsite/admin. Логинимся под суперпользователем, которого создали в пунке 5.1. Далее в раздел мотоциклы, все выделяем галочкой и выполняем команду: "Опубликовать"<p>
<p>8. Снова заходим на сайт.<p>
