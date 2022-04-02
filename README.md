# Скачивание EPIC-фотографий с сайта NASA и отправка сообщений в канал Telegram

Код публикует в вашем телеграм канале фотографии каждые 24 часа, которые он скачивает через API с сайта NASA в папку ``/images/epic``. Подробнее об EPIC-фото и документация по ссылке: https://api.nasa.gov/#epic
Также код отправляет сообщение ``Свежие фоточки из космоса`` в телеграмм-канал перед каждой публикацией.

## Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```python
pip install -r requirements.txt
```
Не забудьте создать необходимый файл ``settings.py`` для правильной работы dotenv, документация по ссылке:
``https://pypi.org/project/python-dotenv/``

### Получите токен для работы API:

Укажите данные для получения токена в разделе Generate API Key по ссылке: 
``https://api.nasa.gov/#epic``

Вы получите токен вида: ``sHMo00RbYXY2hVCqs8t3GFaQDoFLij4EA8DPgpbR``
Создайте файл .env в корневой папке и положите туда переменную с полученным токеном
```python
NASA_API_KEY = "sHMo00RbYXY2hVCqs8t3GFaQDoFLij4EA8DPgpbR"
```

Для изменения пути размещения папки с EPIC-фото NASA, поменяйте значение переменной ``EPIC_FILE_PATH`` на другой путь, также добавьте файл с указанием пути к папке с изображениями:
```python
IMAGE_FOLDER = "images"
EPIC_FILE_PATH = "images/epic"
```

**ВНИМАНИЕ** 
Если вы хотите разместить папку с картинками в корневой директории, путь должен начинаться без ``/``, например при значении``epic`` картинки будут сохраняться в ``/epic``

### Получите токен для отправки сообщения в Телеграмм канале:

Для этого создайте бота в ``https://t.me/botfather``
Полученный токен положите файл ``.env`` в переменную:
```python
BOT_API = "5182241323:AAGmG0IOGu2CrUl6zpvvhjjkChf95mSWwb0"
```

Бота необходимо сделать администратором канала, в который вы хотите отправлять сообщение.
Название канала необходимо положить в ``.env`` в переменную: 
```
CHAT_ID = "@spaace_tg"
```

### Другие настройки

Текст сообщения лежит в ``.env`` в переменной:
```python
MESSAGE = "Hello"
```

По умолчанию публикация идет каждые 24 часа. Настройка таймера постинга в
```python
TIMER = 86400
```

**ВНИМАНИЕ**
Фотографии удаляются из папок после публикации

```python
def publish_photo_to_channel(path: str):
    telegram_token = os.getenv("BOT_API")
    chat_id = os.getenv("CHAT_ID")
    bot = telegram.Bot(token=telegram_token)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            #Отправляем фотки по одной
            bot.send_photo(chat_id=chat_id, photo=open(os.path.join(root, name), 'rb'))
            #Удаляем фотку после отправки, чтобы не засорять папку (фотки немаленькие)
            os.remove(os.path.join(root, name))
```

### Запуск кода:

```
python3 main.py
```

# Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.

## Лицензия

Код распространяется свободно согласно MIT License
