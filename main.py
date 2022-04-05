import datetime
import os
import time
import requests
import telegram
import random



from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse


def publish_text_to_channel(text: str, chat_id: str, token: str):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text)


def publish_photo_to_channel(path: str, chat_id: str, token: str, delete_photo: bool):
    bot = telegram.Bot(token=token)
    photos_path = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            photos_path.append(os.path.join(root, name))
    with open(random.choice(photos_path), 'rb') as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)
    if delete_photo:
        os.remove(os.path.join(root, name))


def save_photo(path: str, url: str, token:str, file_name: str):
    Path(path).mkdir(parents=True, exist_ok=True)
    payload = {
        "api_key": token
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(f'{path}/{file_name}', 'wb') as file:
        file.write(response.content)


def get_extension(url: str) -> str:
    path = urlparse(url).path
    filename, ext = os.path.splitext(path)
    return ext


def fetch_spacex_last_launch(path: str):

    def get_latest_launch_photo_urls():
        spacex_api_url = "https://api.spacexdata.com/v4/launches/latest"
        response = requests.get(spacex_api_url)
        response.raise_for_status()
        latest_launch_dict: dict = response.json()
        return latest_launch_dict['links']['flickr']['original']

    for count, url in enumerate(get_latest_launch_photo_urls()):
        file_name = f'spacex{count}.jpg'
        save_photo(path=path, url=url, token="", file_name=file_name)


def get_nasa_apod_photo(path: str, token: str):

    def get_nasa_apod_photo_urls():
        api_url = "https://api.nasa.gov/planetary/apod"
        payload = {
            "api_key": token,
            "count": 5
        }
        response = requests.get(api_url, params=payload)
        response.raise_for_status()
        nasa_apod_response_dict: dict = response.json()
        nasa_apod_photo_urls = []
        for photos_data in nasa_apod_response_dict:
            print(photos_data)
            nasa_apod_photo_urls.append(photos_data["url"])
        return nasa_apod_photo_urls

    for photos_url in get_nasa_apod_photo_urls():
        file_name = os.path.basename(urlparse(photos_url).path)
        save_photo(path=path, token="", url=photos_url, file_name=file_name)


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

    for photo_name, date in get_epic_photo_data().items():
        file_name = f"{photo_name}.png"
        url = f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{photo_name}.png"
        save_photo(path=path, url=url, token=token, file_name=file_name)


def main():
    chat_id = os.getenv("CHAT_ID")
    telegram_token = os.getenv("BOT_API")
    delete_photo = os.getenv("DELETE_AFTER_SEND")
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
        publish_text_to_channel(text=message, chat_id=chat_id, token=telegram_token)
        publish_photo_to_channel(path=image_folder, chat_id=chat_id, token=telegram_token, delete_photo=delete_photo)
        time.sleep(int(delay))


if __name__ == "__main__":
    load_dotenv()
    main()
