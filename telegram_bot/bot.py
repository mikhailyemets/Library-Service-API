import requests


def send_telegram_message(book_title):
    """
    Sends a message that new instance of book was created to the Telegram bot.
    :param book_title:
    :return:
    """
    token = "7131670430:AAHm9egBs0ASAXWBTnPk0uUbesWnTp5UmMY"
    chat_id = "992655456"
    message = f"New book: '{book_title}' was added to the Library!"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=params)

    if response.status_code == 200:
        print("Message sent successfully to Telegram!")
    else:
        print("Error sending message to Telegram.")
