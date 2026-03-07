import os
from motor.motor_asyncio import AsyncIOMotorClient
from models import UserDocument, AIContext

# В будущем вынесем в .env
MONGO_URL = "mongodb://localhost:27017" 
DB_NAME = "ai_lifestyle_bot"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
users_collection = db["users"]

async def get_or_create_user(tg_id: int, username: str | None = None) -> UserDocument:
    """Находит пользователя или создает нового с пустым контекстом."""
    data = await users_collection.find_one({"_id": tg_id})
    
    if data:
        # Pydantic сам разберется с маппингом
        return UserDocument(**data)
    
    # Если юзера нет, создаем "чистый лист"
    # Теперь username может быть None без ругани линтера
    new_user = UserDocument(_id=tg_id, username=username)
    await users_collection.insert_one(new_user.model_dump(by_alias=True))
    return new_user

async def save_user_context(tg_id: int, context: AIContext):
    """Обновляет только поле ai_context у пользователя."""
    await users_collection.update_one(
        {"_id": tg_id},
        {"$set": {"ai_context": context.model_dump()}}
    )