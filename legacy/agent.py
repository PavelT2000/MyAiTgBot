import os
import httpx
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from database import get_or_create_user, save_user_context
from tools import UPDATE_CONTEXT_TOOL

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

PROXY_URL = os.getenv("PROXY_URL", "http://localhost:8000/api/chat")

async def process_user_message(tg_id: int, user_text: str) -> str:
    """Обработка сообщения с сохранением фактов и планированием времени."""
    user_doc = await get_or_create_user(tg_id)
    context = user_doc.ai_context

    # Берем время в UTC
    now = datetime.utcnow()
    # Форматируем его максимально понятно для ИИ
    current_time_str = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    logging.info(f"📤 [USER {tg_id}]: {user_text}")

    system_instruction = (
        f"Твоя цель: {context.core_objective}. "
        f"Твой стиль: {context.persona_state.get('current_style')}. "
        f"ДАННЫЕ О ВРЕМЕНИ: Сейчас {current_time_str} (UTC). " # Четкое указание времени
        f"Факты о пользователе: {', '.join(context.memory_bank.get('user_facts', [])) or 'Пока нет'}. "
        f"Заметки: {context.memory_bank.get('strategic_notes', '')}. "
        
    )

    payload = {
        "contents": [{"role": "user", "parts": [{"text": user_text}]}],
        "system_instruction": system_instruction,
        "tools": [UPDATE_KNOWLEDGE_TOOL]
    }

    async with httpx.AsyncClient(trust_env=False) as client:
        try:
            logging.info(f"🚀 Запрос на прокси: {PROXY_URL}")
            response = await client.post(PROXY_URL, json=payload, timeout=30.0)
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            logging.error(f"❌ Ошибка сети: {e}")
            return "Ошибка связи с ИИ."

    
    raw_answer = result.get("answer", "")
    f_calls = result.get("function_calls")

    logging.info(f"📥 [RAW RESULT]: {result}")

    if f_calls:
        for call in f_calls:
            if call.get("name") == "update_ai_memory":
                args = call.get("args", {})
                logging.info(f"🧠 [AI UPDATING]: {args}")
                
                # 1. Обновляем стиль и заметки[cite: 26]
                context.persona_state["current_style"] = args.get("new_persona_style", context.persona_state["current_style"])
                context.memory_bank["strategic_notes"] = args.get("new_strategic_notes", context.memory_bank["strategic_notes"])
                
                # 2. Обновляем факты (без дубликатов)[cite: 26]
                new_facts = args.get("add_user_facts", [])
                if new_facts:
                    combined = context.memory_bank.get("user_facts", []) + new_facts
                    context.memory_bank["user_facts"] = list(set(combined))
                
                # 3. Планирование времени[cite: 28]
                next_time_str = args.get("next_contact_time")
                max_delay = now + timedelta(hours=24)
                
                if not next_time_str:
                    next_time_str = max_delay.isoformat()
                    logging.info("🕒 Время не указано, ставим +24ч")
                
                context.next_contact_time = next_time_str
                context.is_waiting_contact = True

                await save_user_context(tg_id, context)
                logging.info(f"💾 [SAVED]. Next contact: {next_time_str}")

# --- ИСПРАВЛЕНИЕ PYLANCE И ПУСТОГО ОТВЕТА ---
    
    # Случай А: ИИ вызвал функцию, но текста нет (или там "Пустой ответ")
    if (not raw_answer or raw_answer.strip() == "Пустой ответ") and f_calls:
        return "🤖 Принято! Я обновил свою память и запланировал следующий шаг."
    
    # Случай Б: Есть нормальный текстовый ответ
    if raw_answer and raw_answer.strip() != "Пустой ответ":
        return raw_answer

    # Случай В: Fallback (если вообще ничего нет), чтобы не вернуть None
    return "ИИ выполнил задачу, но не оставил сообщения."