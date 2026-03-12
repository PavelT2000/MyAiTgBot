# tools.py

# Это описание функции для Gemini. 
# Оно говорит ИИ: "У тебя есть доступ к редактированию своего сознания".
# UPDATE_CONTEXT_TOOL = {
#     "name": "update_ai_memory",
#     "description": "Обнови свою внутреннюю личность, факты о пользователе и стратегию поведения.",
#     "parameters": {
#         "type": "OBJECT",
#         "properties": {
#             "new_persona_style": {"type": "STRING", "description": "Твой новый стиль общения"},
#             "add_user_facts": {"type": "ARRAY", "items": {"type": "STRING"}, "description": "Новые факты, которые ты узнал"},
#             "new_strategic_notes": {"type": "STRING", "description": "Твои мысли о том, как лучше вести пользователя к цели"}
#         },
#         "required": ["new_persona_style"]
#     }
# }

# UPDATE_CONTEXT_TOOL = {
#     "name": "update_ai_memory",
#     "description": "Обнови память и запланируй время следующего сообщения.",
#     "parameters": {
#         "type": "OBJECT",
#         "properties": {
#             "new_persona_style": {"type": "STRING"},
#             "add_user_facts": {"type": "ARRAY", "items": {"type": "STRING"}},
#             "new_strategic_notes": {"type": "STRING"},
#             "next_contact_time": {
#                 "type": "STRING", 
#                 "description": "Время в формате ISO (например: 2026-03-07T10:00:00). Если не нужно - не заполняй."
#             }
#         },
#         "required": ["new_persona_style"]
#     }
# }
UPDATE_KNOWLEDGE_TOOL = {
    "name": "update_knowledge_base",
    "description": "Управление долгосрочной памятью. Позволяет сохранять факты с оценкой их достоверности.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "updates": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "category": {
                            "type": "STRING", 
                            "description": "Категория знания (health, work, bio, habits)"
                        },
                        "value": {
                            "description": "Содержание факта. ОДИН факт = ОДНО простое утверждение. "
                            "НЕ ПИШИ причины и следствия в одном факте. "
                            "Вместо 'Худой из-за метаболизма' пиши: 'Худощавое телосложение' и 'Быстрый метаболизм'."
                        },
                        "action": {
                            "type": "STRING",
                            "enum": ["add", "update", "mark_obsolete"],
                            "description": "Что сделать с этим фактом"
                        },
                        "confidence": {
                            "type": "NUMBER",
                            "description": "Твоя уверенность в факте от 0.0 до 1.0. "
                                           "0.2 - догадка, 0.5 - упомянуто вскользь, "
                                           "1.0 - четкое утверждение пользователя."
                        }
                    },
                    "required": ["category", "value", "action", "confidence"]
                }
            },
            "behavioral_shift": {
                "type": "STRING",
                "description": "Описание изменения тона или стиля."
            }
        },
        "required": ["updates"]
    }
}