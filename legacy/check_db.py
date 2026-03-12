import asyncio
from database import get_or_create_user, save_user_context
from models import AIContext

async def check_database_flow():
    print("🚀 Начинаем проверку MongoDB...")
    
    # 1. Тестовые данные
    TEST_ID = 999
    TEST_NAME = "Tester"
    
    print(f"\n[1] Пытаемся создать/получить юзера с ID {TEST_ID}...")
    user = await get_or_create_user(TEST_ID, TEST_NAME)
    print(f"✅ Успех! Имя в базе: {user.username}")
    print(f"Текущий стиль ИИ: {user.ai_context.persona_state['current_style']}")

    # 2. Имитируем «обучение» нейронки
    print(f"\n[2] Имитируем обновление контекста нейронкой...")
    user.ai_context.persona_state["current_style"] = "Кибер-психолог"
    user.ai_context.persona_state["evolution_stage"] = 2
    user.ai_context.memory_bank["user_facts"].append("Тестирует базу в 2026 году")
    user.ai_context.memory_bank["strategic_notes"] = "Пользователь склонен к системному подходу."

    # 3. Сохраняем
    print("[3] Сохраняем обновленный 'мозг' в базу...")
    await save_user_context(TEST_ID, user.ai_context)
    print("✅ Данные отправлены в MongoDB.")

    # 4. Проверяем чистым чтением
    print(f"\n[4] Считываем данные заново для проверки...")
    fresh_user = await get_or_create_user(TEST_ID)
    
    print(f"--- РЕЗУЛЬТАТ ---")
    print(f"ID: {fresh_user.id}")
    print(f"Новый стиль: {fresh_user.ai_context.persona_state['current_style']}")
    print(f"Этап эволюции: {fresh_user.ai_context.persona_state['evolution_stage']}")
    print(f"Факты в памяти: {fresh_user.ai_context.memory_bank['user_facts']}")
    print(f"Заметки: {fresh_user.ai_context.memory_bank['strategic_notes']}")
    
    if fresh_user.ai_context.persona_state["current_style"] == "Кибер-психолог":
        print("\n🔥 ПРОВЕРКА ПРОЙДЕНА: База работает, типы данных сохраняются корректно!")
    else:
        print("\n❌ ОШИБКА: Данные не обновились.")

if __name__ == "__main__":
    try:
        asyncio.run(check_database_flow())
    except Exception as e:
        print(f"\n❌ Ошибка подключения: {e}")
        print("Проверь, запущен ли сервер MongoDB и доступен ли порт 27017.")