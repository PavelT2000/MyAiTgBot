import asyncio
import logging
from datetime import datetime
from database import users_collection
from legacy.ai_agent import process_user_message
from bot import bot

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def check_planned_events():
    """Фоновый процесс проверки запланированных сообщений."""
    logging.info("🚀 Планировщик запущен и мониторит базу...")
    
    while True:
        try:
            now = datetime.utcnow()
            # Ищем юзеров, чье время пришло
            query = {
                "ai_context.next_contact_time": {"$lte": now.isoformat()},
                "ai_context.is_waiting_contact": True
            }
            
            cursor = users_collection.find(query)
            users_found = await cursor.to_list(length=100) # Для асинхронного motor

            if users_found:
                logging.info(f"🔔 Найдено {len(users_found)} задач для отправки.")
                
                for user_data in users_found:
                    tg_id = user_data["_id"]
                    logging.info(f"🤖 ИИ инициирует контакт с {tg_id}...")

                    prompt = "[СИСТЕМНОЕ: Время вышло. Напиши пользователю первым, исходя из твоих целей.]"
                    ai_response = await process_user_message(tg_id, prompt)

                    try:
                        await bot.send_message(tg_id, ai_response)
                        logging.info(f"✅ Сообщение отправлено пользователю {tg_id}")
                    except Exception as send_error:
                        logging.error(f"❌ Не удалось отправить сообщение {tg_id}: {send_error}")

                    # Сбрасываем флаг ожидания
                    await users_collection.update_one(
                        {"_id": tg_id},
                        {"$set": {"ai_context.is_waiting_contact": False}}
                    )
            else:
                # Тихий лог, чтобы не забивать консоль, если пусто
                # logging.debug("Очередь пуста...")
                pass

        except Exception as e:
            logging.error(f"❌ КРИТИЧЕСКАЯ ОШИБКА ПЛАНИРОВЩИКА: {e}")
            
        await asyncio.sleep(60) # Проверка раз в минуту

if __name__ == "__main__":
    asyncio.run(check_planned_events())