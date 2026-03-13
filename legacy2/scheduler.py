"""
Module that shedule events
"""
from typing import Callable, Any, Awaitable, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from config import config
MessageHandlerType = Callable[[int, str], Awaitable[Any]]
planned_message_handler: Optional[MessageHandlerType] = None

# Настройка хранения задач в MongoDB, чтобы они не удалялись при перезагрузке
jobstores = {
    'default': MongoDBJobStore(
        database='ai_bot',
        collection='scheduled_jobs',
        host=config.mongo_url
        )
}

scheduler = AsyncIOScheduler(jobstores=jobstores)


async def send_planned_message_to_user(user_id: int, text: str):
    """Эта функция вызывается планировщиком"""
    if planned_message_handler is not None:
        await planned_message_handler(user_id, text)
    else:
        print(f"⚠️ Ошибка: Обработчик отправки не установлен! (User: {user_id})")

async def send_silence_signal_to_ai(user_id:int):
    """Отправляет ии сообщение о молчании пользователя"""
