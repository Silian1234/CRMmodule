import telegram
from django.conf import settings
import asyncio

BOT_TOKEN = '7561138849:AAGUOHPySU5af54NkE27t7IcC2xJxVgGfvY'
bot = telegram.Bot(token=BOT_TOKEN)

async def send_notification_to_user(user_telegram_link, message_text):
    try:
        await bot.send_message(chat_id=user_telegram_link, text=message_text)
        print(f"Уведомление отправлено пользователю: {user_telegram_link}")
    except Exception as e:
        print(f"Ошибка при отправке уведомления пользователю {user_telegram_link}: {e}")

