"""
Module that interacts with ai api
"""
from datetime import datetime, timedelta
import logging
import httpx
from embedding import get_embedding
from config import config

proxy_logger=logging.getLogger('proxy')

async def process_ai_function(payload, context, user_id):
    """
    procesing function of ai
    """
    async with httpx.AsyncClient(trust_env=False) as client:
        proxy_logger.info("🚀 Запрос на прокси: %s", config.api_chat_url)
        response = await client.post(config.api_chat_url, json=payload, timeout=30.0)
        response.raise_for_status()
        result = response.json()

    has_functions = False
    if result.get("function_calls"):
        has_functions = True
        for call in result["function_calls"]:
            if call["name"] == "update_knowledge_base":
                updates = call["args"].get("updates", [])
                for fact in updates:
                    vector = await get_embedding(fact["value"])
                    fact_data = {
                        "text": fact["value"],
                        "embedding": vector,
                        "timestamp": datetime.utcnow().isoformat(),
                        "category": fact["category"]
                    }
                    context.memory_bank["user_facts"].append(fact_data)
                print(f"✅ В user_facts сохранено {len(updates)} фактов.")
            if call["name"] == "schedule_reminder":
                args = call["args"]
                run_at = datetime.now() + timedelta(minutes=args.get("delay_minutes", 60))
                scheduler.add_job(
                    send_planned_message,
                    'date',
                    run_date=run_at,
                    args=[user_id, args.get("message")],
                    # Один юзер — одна активная напоминалка (перезаписывает старую)
                    id=f"remind_{user_id}",
                    replace_existing=True
                )
                print(f"📅 Запланировано: {args.get('message')} на {run_at}")

    # Возвращаем и текст, и флаг, был ли вызов функции
    return result.get('answer', ''), has_functions
