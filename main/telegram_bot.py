import telebot
from django.conf import settings
import asyncio
import requests, json

BOT_TOKEN = '7561138849:AAGUOHPySU5af54NkE27t7IcC2xJxVgGfvY'
bot = telebot.TeleBot(token=BOT_TOKEN)
user = None
async def send_notification_to_user(user_telegram_link, message_text):
    user = user_telegram_link.split('@')[1]
    url = "https://api.telegram.org/bot7561138849:AAGUOHPySU5af54NkE27t7IcC2xJxVgGfvY/getUpdates"
    page = requests.get(url)
    text = page.json()
    for i in text["result"]:
        if i["message"]["from"]["username"] == user:
            id = i["message"]["from"]["id"]
    try:
        await bot.send_message(chat_id=id, text=message_text)
        print(f"Уведомление отправлено пользователю: {user_telegram_link}")
    except Exception as e:
        print(f"Ошибка при отправке уведомления пользователю {user_telegram_link}: {e}")
