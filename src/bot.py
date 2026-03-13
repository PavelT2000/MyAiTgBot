"""
bot module, uses aiogram
"""
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from src.config import config
from src.logger_config import setup_logging
from src.api import process_user_message

bot = Bot(token=config.telegram_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    """Приветственное сообщение."""
    await message.answer("Привет! Я слежу за нашим диалогом. Если ты замолчишь на 10 минут, я попробую продолжить сам.")

@dp.message()
async def message_handler(message: types.Message):
    """Основной обработчик сообщений."""
    if not message.from_user or not message.text:
        return
    await bot.send_chat_action(message.chat.id, "typing")
    tg_id=message.from_user.id
    answer=await process_user_message(user_id=tg_id,message=message.text)
    if answer:
        await message.answer(answer)

async def main():
    """Запуск бота."""
    setup_logging()


    print("📅 Планировщик запущен")
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())