import asyncio
import os
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from ai_agent import process_user_message

load_dotenv()

# 1. Исправляем ошибку с токеном
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    print("❌ ОШИБКА: TELEGRAM_TOKEN не найден в файле .env")
    sys.exit(1)

bot = Bot(token=TOKEN)
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

async def main():
    """Запуск бота."""
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())