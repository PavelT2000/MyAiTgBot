"""
module that afford embed(vectorize) text and facts
"""
from datetime import datetime
import httpx
import numpy as np
from src.config import config

async def get_embedding(text: str):
    """Получает вектор из фразы"""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            config.embed_url,
            json={"text": text, "task_type": "RETRIEVAL_DOCUMENT"}
            )
        return resp.json().get("embedding")

async def get_relevant_facts(user_facts: dict, user_text: str, n: int = 5):
    """
    Принимает факты, текст сообщения, кол-во необходимых фактов
    Находит все ближайшие факты к тексту сообщения.
    """
    if not user_facts:
        return []

    # 2. Получаем вектор текущего вопроса (Query)
    async with httpx.AsyncClient() as client:
        resp = await client.post(config.embed_url, json={
            "text": user_text,
            "task_type": "RETRIEVAL_QUERY"
        })
        query_vector = resp.json().get("embedding")

    q_vec = np.array(query_vector)
    scored_facts = []
    now = datetime.utcnow()

    # 3. Ранжируем: Смысл (80%) + Время (20%)
    for f in user_facts:
        if "embedding" not in f or f["embedding"] is None:
            continue
        f_vec = np.array(f["embedding"])
        # Косинусное сходство
        sim = np.dot(q_vec, f_vec) / (np.linalg.norm(q_vec) * np.linalg.norm(f_vec))

        # Recency Score (затухание)
        f_time = datetime.fromisoformat(f["timestamp"])
        days_old = (now - f_time).days
        # Чем свежее, тем ближе к 1.0 (затухает на ~2% в день)
        recency = np.exp(-0.02 * days_old)

        # Итоговый скор
        final_score = (sim * 0.8) + (recency * 0.2)

        # Создаем копию словаря БЕЗ эмбеддинга
        fact_data = {k: v for k, v in f.items() if k != "embedding"}
        scored_facts.append((final_score, fact_data))

    # 4. Сортируем по убыванию и возвращаем n штук
    scored_facts.sort(key=lambda x: x[0], reverse=True)
    return [text for score, text in scored_facts[:n]]
