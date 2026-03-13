"""
Main module that starts bot and tracks user silence.
"""
import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import scheduler
from config import config
from logger_config import setup_logging
from silence_checker import reset_silence_timer

# Заглушка вместо реального вызова ИИ
async def process_user_message_stub(user_id: int, text: str) -> str:
    """Заглушка для обработки сообщений ИИ."""
    if "[SYSTEM_SILENCE_10M]" in text:
        return "Прошло 10 минут тишины. Я решил напомнить о себе! О чем думаешь?"
    return f"Эхо-ответ на: {text}"

bot = Bot(token=config.telegram_token)
dp = Dispatcher()

async def check_silence_handler(user_id: int):
    """
    Вызывается автоматически через 10 минут тишины пользователя.
    """
    print(f"🕵️ Пользователь {user_id} молчит 10 минут. Запрашиваем реакцию ИИ...")

    # Вызываем ИИ с системной пометкой
    ai_response = await process_user_message_stub(user_id, "[SYSTEM_SILENCE_10M]")

    if ai_response:
        try:
            await bot.send_message(chat_id=user_id, text=ai_response)
        except Exception as e:
            print(f"❌ Не удалось отправить сообщение тишины: {e}")

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    """Приветственное сообщение."""
    await message.answer("Привет! Я слежу за нашим диалогом. Если ты замолчишь на 10 минут, я попробую продолжить сам.")

@dp.message()
async def message_handler(message: types.Message):
    """Основной обработчик сообщений."""
    if not message.from_user or not message.text:
        return

    tg_id = message.from_user.id
    user_text = message.text

    await reset_silence_timer(tg_id)


    await bot.send_chat_action(message.chat.id, "typing")

    # Вызов заглушки (в будущем замени на реальный process_user_message)
    ai_response = await process_user_message_stub(tg_id, user_text)

    await message.answer(ai_response)

async def scheduled_send_handler(user_id: int, text: str):
    """Реальная отправка сообщения через объект bot (для других напоминаний)"""
    try:
        await bot.send_message(chat_id=user_id, text=text)
        print(f"🔔 Сообщение по расписанию отправлено для {user_id}")
    except Exception as e:
        print(f"❌ Ошибка отправки по расписанию: {e}")

async def main():
    """Запуск бота."""
    setup_logging()

    # Регистрируем обработчик для scheduler_config
    scheduler.planned_message_handler = scheduled_send_handler

    # Запускаем планировщик
    scheduler.scheduler.start()

    print("📅 Планировщик запущен")
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())