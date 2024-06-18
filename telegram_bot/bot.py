import requests
from decouple import config


def send_telegram_file(file_path: str, token: str, chat_id: str) -> None:
    """
    Sends a file to the Telegram bot.
    :param file_path: The path to the file to be sent.
    :param token: Token of the Telegram bot.
    :param chat_id: The chat id where the file will be sent.
    :return:
    """
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(file_path, 'rb') as file:
        response = requests.post(url, data={"chat_id": chat_id}, files={"document": file})


def send_telegram_message(message: str) -> None:
    """
    Sends a message to the Telegram bot depending on the object type.
    :param message: The message to be sent.
    :return:
    """
    token = config("TG_TOKEN", default="1234")
    chat_id = config("TG_CHAT_ID", default="1234")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=params)
