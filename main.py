import datetime
import os
import requests
import telegram


from dotenv import load_dotenv
from pathlib import Path


def publish_text_to_channel(text: str):
    telegram_token = os.getenv("BOT_API")
    chat_id = os.getenv("CHAT_ID")
    bot = telegram.Bot(token=telegram_token)
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


def get_epic_photo(path: str, token: str):

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
        file_name = f"nasa_apod{photo_name}.png"
        url = f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{photo_name}.png"
        save_photo(url=url, file_name=file_name)


def main():
    epic_file_path = os.getenv("EPIC_FILE_PATH")
    nasa_api_key = os.getenv("NASA_API_KEY")
    message = os.getenv("MESSAGE")
    get_epic_photo(path=epic_file_path, token=nasa_api_key)
    publish_text_to_channel(text=message)


if __name__ == "__main__":
    load_dotenv()
    main()
