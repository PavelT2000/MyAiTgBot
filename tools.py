# tools.py

# Это описание функции для Gemini. 
# Оно говорит ИИ: "У тебя есть доступ к редактированию своего сознания".
UPDATE_CONTEXT_TOOL = {
    "name": "update_ai_memory",
    "description": "Обнови свою внутреннюю личность, факты о пользователе и стратегию поведения.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "new_persona_style": {"type": "STRING", "description": "Твой новый стиль общения"},
            "add_user_facts": {"type": "ARRAY", "items": {"type": "STRING"}, "description": "Новые факты, которые ты узнал"},
            "new_strategic_notes": {"type": "STRING", "description": "Твои мысли о том, как лучше вести пользователя к цели"}
        },
        "required": ["new_persona_style"]
    }
}

UPDATE_CONTEXT_TOOL = {
    "name": "update_ai_memory",
    "description": "Обнови память и запланируй время следующего сообщения.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "new_persona_style": {"type": "STRING"},
            "add_user_facts": {"type": "ARRAY", "items": {"type": "STRING"}},
            "new_strategic_notes": {"type": "STRING"},
            "next_contact_time": {
                "type": "STRING", 
                "description": "Время в формате ISO (например: 2026-03-07T10:00:00). Если не нужно - не заполняй."
            }
        },
        "required": ["new_persona_style"]
    }
}