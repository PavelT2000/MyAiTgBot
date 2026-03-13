"""
Main module that starts bot
"""
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import scheduler_config
from config  import config
from process_user_message import process_user_message
from logger_config import setup_logging

bot = Bot(token=config.telegram_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    """Приветственное сообщение."""
    await message.answer("Привет! Я     твой самообучающийся ИИ-агент. Напиши мне что-нибудь.")

@dp.message()
async def message_handler(message: types.Message):
    """Основной обработчик сообщений."""
    # 2. Исправляем ошибку с None в id и тексте
    if not message.from_user or not message.text:
        return

    await bot.send_chat_action(message.chat.id, "typing")
    tg_id = message.from_user.id
    user_text = message.text
    # Теперь Pylance спокоен: tg_id — это int, user_text — это str
    ai_response = await process_user_message(tg_id, user_text)
    await message.answer(ai_response)

async def scheduled_send_handler(user_id: int, text: str):
    """Реальная отправка сообщения через объект bot"""
    try:
        await bot.send_message(chat_id=user_id, text=text)
        print(f"🔔 Сообщение по расписанию отправлено для {user_id}")
    except Exception as e:
        print(f"❌ Ошибка отправки по расписанию: {e}")

async def main():
    """Запуск бота."""
    setup_logging()
    scheduler_config.send_planned_message=scheduled_send_handler
    scheduler_config.scheduler.start()
    print("📅 Планировщик запущен")
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
