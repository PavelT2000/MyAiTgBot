
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from src.config import config
from src.api.models import MongoDBUser
logger = logging.getLogger('database')


client = AsyncIOMotorClient(config.mongo_url)
db = client[config.mongo_db_name]
users_collection = db["users"]

async def get_or_create_user(tg_id: int, username: str | None = None) -> MongoDBUser :
    """Находит пользователя или создает нового с пустым контекстом."""
    data = await users_collection.find_one({"_id": tg_id})
    if data:
        return MongoDBUser(**data)
    new_user = MongoDBUser(_id=tg_id, username=username)
    await users_collection.insert_one(new_user.model_dump(by_alias=True))
    return new_user

async def save_user_context(tg_id: int, context: MongoDBUser):
    """Обновляет только поле ai_context у пользователя."""
    await users_collection.update_one(
        {"_id": tg_id},
        {"$set": {"user_data": context.model_dump()}}
    )
    context_str = str(context.model_dump())
    logger.info("💾 Контекст сохранен для %s: %s...",tg_id,context_str[:50])
