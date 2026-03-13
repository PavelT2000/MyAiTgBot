from models import UserDocument, MemoryEntry
from datetime import datetime

class MemoryManager:
    @staticmethod
    def get_summary(context) -> str:
        """Превращает сложные объекты MemoryEntry в строку для промпта."""
        facts = [f"{m.category}: {m.value}" for m in context.memory_bank.values() if m.confidence > 0.2]
        return "; ".join(facts) if facts else "Память пуста."

    @staticmethod
    async def process_calls(user: UserDocument, f_calls: list):
        """Разбирает аргументы от ИИ и обновляет модель данных."""
        for call in f_calls:
            if call["name"] == "update_ai_memory":
                args = call.get("args", {})
                
                # Обновляем стиль
                if "new_persona_style" in args:
                    user.ai_context.persona_state.current_style = args["new_persona_style"]
                
                # Умное обновление фактов
                new_facts = args.get("add_user_facts", [])
                for fact_text in new_facts:
                    # Логика: если такой факт (примерно) есть - повышаем уверенность
                    # Для упрощения пока используем текст как ключ
                    key = fact_text.lower().strip()
                    if key in user.ai_context.memory_bank:
                        user.ai_context.memory_bank[key].confidence = min(1.0, user.ai_context.memory_bank[key].confidence + 0.3)
                        user.ai_context.memory_bank[key].updated_at = datetime.utcnow()
                    else:
                        user.ai_context.memory_bank[key] = MemoryEntry(
                            value=fact_text, 
                            category="observation" # ИИ может передавать категорию, если расширить Tool
                        )
                
                # Планирование
                if "next_contact_time" in args:
                    try:
                        user.ai_context.next_contact_time = datetime.fromisoformat(args["next_contact_time"])
                        user.ai_context.is_waiting_contact = True
                    except:
                        pass