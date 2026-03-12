from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
import os

planned_message_handler = None

# Настройка хранения задач в MongoDB, чтобы они не удалялись при перезагрузке
jobstores = {
    'default': MongoDBJobStore(database='ai_bot', collection='scheduled_jobs', host=os.getenv("MONGO_URI"))
}

scheduler = AsyncIOScheduler(jobstores=jobstores)


async def send_planned_message(user_id: int, text: str):
    """Эта функция вызывается планировщиком"""
    if planned_message_handler:
        await planned_message_handler(user_id, text)
    else:
        print(f"⚠️ Ошибка: Обработчик отправки не установлен! (User: {user_id})")