import datetime
import os
import time

import requests
import telegram


from dotenv import load_dotenv
from pathlib import Path


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
            #Отправляем фотки по одной
            bot.send_photo(chat_id=chat_id, photo=open(os.path.join(root, name), 'rb'))
            #Удаляем фотку после отправки, чтобы не засорять папку (фотки немаленькие)
            os.remove(os.path.join(root, name))


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
    image_folder = os.getenv("IMAGE_FOLDER")
    epic_file_path = os.getenv("EPIC_FILE_PATH")
    nasa_api_key = os.getenv("NASA_API_KEY")
    message = os.getenv("MESSAGE")
    delay = os.getenv("TIMER")
    go = True
    while go:
        get_epic_nasa_photo(path=epic_file_path, token=nasa_api_key)
        publish_text_to_channel(text=message)
        publish_photo_to_channel(path=image_folder)
        time.sleep(delay)


if __name__ == "__main__":
    load_dotenv()
    main()
