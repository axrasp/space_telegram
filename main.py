import datetime
import os
import time
import requests
import telegram


from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse

SPACEX_API_URL = "https://api.spacexdata.com/v4/launches/latest"
NASA_APOD_API_URL = "https://api.nasa.gov/planetary/apod"


def publish_text_to_channel(text: str):
    telegram_token = os.getenv("BOT_API")
    chat_id = os.getenv("CHAT_ID")
    bot = telegram.Bot(token=telegram_token)
    bot.send_message(chat_id=chat_id, text=text)


def publish_photo_to_channel(path: str):
    telegram_token = os.getenv("BOT_API")
    chat_id = os.getenv("CHAT_ID")
    bot = telegram.Bot(token=telegram_token)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            # Отправляем фотки по одной
            bot.send_photo(chat_id=chat_id, photo=open(os.path.join(root, name), 'rb'))
            # Уберите комментарий следующей строки, чтобы автоматически удалять фотки после отправки, чтобы не засорять папку (фотки немаленькие)
            # os.remove(os.path.join(root, name))


def get_extension(url: str) -> str:
    path = urlparse(url).path
    filename, ext = os.path.splitext(path)
    return ext


def fetch_spacex_last_launch(path: str):

    def get_latest_launch_photo_urls():
        response = requests.get(SPACEX_API_URL)
        response.raise_for_status()
        latest_launch_dict: dict = response.json()
        return latest_launch_dict['links']['flickr']['original']

    def save_photo(image_folder_path: str, url: str, file_name: str):
        Path(image_folder_path).mkdir(parents=True, exist_ok=True)
        response = requests.get(url)
        response.raise_for_status()
        with open(f'{image_folder_path}/{file_name}', 'wb') as file:
            file.write(response.content)

    for count, url in enumerate(get_latest_launch_photo_urls()):
        file_name = f'spacex{count}.jpg'
        save_photo(image_folder_path=path, url=url, file_name=file_name)


def get_nasa_apod_photo(path: str, token: str):

    def get_nasa_apod_photo_urls():
        api_url = NASA_APOD_API_URL
        payload = {
            "api_key": token,
            "count": 5
        }
        response = requests.get(api_url, params=payload)
        response.raise_for_status()
        nasa_apod_response_dict: dict = response.json()
        nasa_apod_photo_urls = []
        for photos_data in nasa_apod_response_dict:
            nasa_apod_photo_urls.append(photos_data["url"])
        return nasa_apod_photo_urls

    def save_photo(path: str, url: str):
        Path(path).mkdir(parents=True, exist_ok=True)
        response = requests.get(url)
        response.raise_for_status()
        file_name = os.path.basename(urlparse(url).path)
        with open(f"{path}/{file_name}", "wb") as file:
            file.write(response.content)

    for photos_url in get_nasa_apod_photo_urls():
        save_photo(path=path, url=photos_url)


def get_epic_nasa_photo(path: str, token: str):

    def get_epic_photo_data():
        api_url = "https://api.nasa.gov/EPIC/api/natural/images"
        payload = {
            "api_key": token
        }
        response = requests.get(api_url, params=payload)
        response.raise_for_status()
        photo_dict = {}
        nasa_apod_response_dict: dict = response.json()
        for keys in nasa_apod_response_dict:
            photo_dict[keys["image"]] = datetime.datetime.fromisoformat(keys["date"]).strftime("%Y/%m/%d")
        return photo_dict

    def save_photo(url: str, file_name: str):
        Path(path).mkdir(parents=True, exist_ok=True)
        payload = {
            "api_key": token
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        with open(f"{path}/{file_name}", "wb") as file:
            file.write(response.content)

    for photo_name, date in get_epic_photo_data().items():
        file_name = f"{photo_name}.png"
        url = f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{photo_name}.png"
        save_photo(url=url, file_name=file_name)


def main():
    nasa_api_key = os.getenv("NASA_API_KEY")
    nasa_apod_image_path = os.getenv("NASA_APOD_PATH")
    image_folder = os.getenv("IMAGE_FOLDER")
    epic_file_path = os.getenv("EPIC_FILE_PATH")
    message = os.getenv("MESSAGE")
    delay = os.getenv("TIMER")
    go = True
    while go:
        fetch_spacex_last_launch(path=image_folder)
        get_nasa_apod_photo(path=nasa_apod_image_path, token=nasa_api_key)
        get_epic_nasa_photo(path=epic_file_path, token=nasa_api_key)
        publish_text_to_channel(text=message)
        publish_photo_to_channel(path=image_folder)
        time.sleep(int(delay))


if __name__ == "__main__":
    load_dotenv()
    main()
