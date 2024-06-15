import requests


def send_telegram_message(message: str) -> None:
    """
    Sends a message to the Telegram bot depending on the object type.
    :param message: The message to be sent.
    :return:
    """
    token = '7131670430:AAHm9egBs0ASAXWBTnPk0uUbesWnTp5UmMY'
    chat_id = '992655456'

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=params)

    if response.status_code == 200:
        print("Message sent successfully to Telegram!")
    else:
        print("Error sending message to Telegram.")
