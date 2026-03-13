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

SCHEDULE_REMINDER_TOOL = {
    "name": "schedule_reminder",
    "description": "Запланировать отправку сообщения пользователю через определенное время, чтобы продолжить диалог или проверить прогресс.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Текст сообщения, которое нужно отправить пользователю позже."
            },
            "delay_minutes": {
                "type": "integer",
                "description": "Через сколько минут отправить сообщение (например, 30, 60, 1440)."
            },
            "context_note": {
                "type": "string",
                "description": "Краткая заметка для себя, о чем будет этот контакт (например, 'спросить про яблоки')."
            }
        },
        "required": ["message", "delay_minutes"]
    }
}