# Скачивание EPIC-фотографий с сайта NASA

Код позволяет скачать EPIC-фото через API с сайта NASA в папку ``/epic``. Подробнее об EPIC-фото и документация по ссылке: https://api.nasa.gov/#epic

## Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```
Не забудьте создать необходимый файл ``settings.py`` для правильной работы dotenv, документация по ссылке:
``https://pypi.org/project/python-dotenv/``

### Получите токен для работы API:

Укажите данные для получения токена в разделе Generate API Key по ссылке: 
``https://api.nasa.gov/#epic``

Вы получите токен вида:

```
sHMo00RbYXY2hVCqs8t3GFaQDoFLij4EA8DPgpbR
```
Создайте файл .env в корневой папке и положите туда переменную с полученным токеном

```
NASA_API_KEY = sHMo00RbYXY2hVCqs8t3GFaQDoFLij4EA8DPgpbR

```

Для изменения пути сохранения файла, поменяйте значение переменной ``EPIC_FILE_PATH`` на другой путь. 

**ВНИМАНИЕ** 
Если вы хотите разместить папку с картинками в корневой директории, путь должен начинаться без ``/``, например при значении``epic`` картинки будут сохраняться в ``/epic``

### Запуск кода:

```
python3 main.py
```

# Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.

## Лицензия

Код распространяется свободно согласно MIT License