import httpx

async def get_relevant_facts(user_facts: dict, user_text: str, n: int = 5):
    """
    Принимает текст вопроса и количество фактов.
    Сама лезет в БД, векторизует запрос и ранжирует факты.
    """

    if not user_facts:
        return []

    # 2. Получаем вектор текущего вопроса (Query)
    EMBED_URL = "http://ai.pavelzabelich.ru/api/embed"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(EMBED_URL, json={
                "text": user_text, 
                "task_type": "RETRIEVAL_QUERY"
            })
            query_vector = resp.json().get("embedding")
        except Exception as e:
            print(f"Ошибка векторизации запроса: {e}")
            return [f["text"] for f in user_facts[:n]]

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
