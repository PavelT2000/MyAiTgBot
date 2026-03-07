import asyncio
from database import get_or_create_user, save_user_context

async def test_db():
    print("--- Тест Базы Данных ---")
    
    user_id = 123456789  # Твой или тестовый ID
    
    # 1. Получаем/Создаем юзера
    user = await get_or_create_user(user_id, "AlexTest")
    print(f"Загружен юзер {user.id}. Стиль ИИ: {user.ai_context.persona_state['current_style']}")
    
    # 2. Имитируем, что нейронка что-то узнала и изменила свой контекст
    user.ai_context.persona_state["current_style"] = "Активный коуч"
    user.ai_context.memory_bank["user_facts"].append("Ложится спать после полуночи")
    
    # 3. Сохраняем изменения
    await save_user_context(user_id, user.ai_context)
    print("Контекст обновлен и сохранен в MongoDB.")
    
    # 4. Проверяем повторным чтением
    updated_user = await get_or_create_user(user_id)
    print(f"Повторное чтение. Новый стиль: {updated_user.ai_context.persona_state['current_style']}")
    print(f"Факты: {updated_user.ai_context.memory_bank['user_facts']}")

if __name__ == "__main__":
    asyncio.run(test_db())