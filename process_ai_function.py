import httpx
import logging
from embedding import get_embedding
from datetime import datetime
from config import API_CHAT_URL

proxy_logger=logging.getLogger('proxy')

async def process_ai_function(payload, context):
    async with httpx.AsyncClient(trust_env=False) as client:
        proxy_logger.info("🚀 Запрос на прокси: %s",API_CHAT_URL)
        response = await client.post(API_CHAT_URL, json=payload, timeout=30.0)
        response.raise_for_status()
        result = response.json()
        
    if result.get("function_calls"):
        for call in result["function_calls"]:
            if call["name"] == "update_knowledge_base":
                updates = call["args"].get("updates", [])
                
                for fact in updates:
                    # 1. Получаем вектор (для будущего RAG)
                    vector = await get_embedding(fact["value"])
                    
                    # 2. Создаем объект факта
                    fact_data = {
                        "text": fact["value"],
                        "embedding": vector,
                        "timestamp": datetime.utcnow().isoformat(), # Сериализуем для JSON
                        "category": fact["category"]
                    }
                    
                    # 3. Сохраняем прямо в список фактов в контексте
                    context.memory_bank["user_facts"].append(fact_data)
                
                # Сохраняем обновленный контекст в БД

                print(f"✅ В user_facts сохранено {len(updates)} фактов с векторами.")
    return result.get('answer','')