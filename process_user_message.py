import logging
from tools import UPDATE_KNOWLEDGE_TOOL
from database import get_or_create_user, save_user_context
from embedding import get_relevant_facts
from process_ai_function import process_ai_function



service_logger=logging.getLogger('service')


async def process_user_message(user_id: int, message_text: str)->str:
    user_doc = await get_or_create_user(user_id)
    context = user_doc.ai_context    
    relevant_facts = await get_relevant_facts(context.memory_bank.get('user_facts', []), message_text, n=100)
    # Форматируем каждый факт в строку для промпта
    facts_strings = []
    for f in relevant_facts:
        # Собираем инфу: текст + (метаданные)
        meta = f"[{f.get('category', 'общие')}, ув: {f.get('confidence', '?')}]"
        facts_strings.append(f"- {f['text']} {meta}")
        
    system_instruction = (
            f"Твоя цель: Сделать жизнь пользователя лучше, вести себя подобно человеку"
            # f"Твой стиль: {context.persona_state.get('current_style')}. "
            # f"ДАННЫЕ О ВРЕМЕНИ: Сейчас {current_time_str} (UTC). " # Четкое указание времени
            f"Факты о пользователе: {'\n'.join(facts_strings) or 'Нет данных.'}. "
            f"Заметки: {context.memory_bank.get('strategic_notes', '')}. "
            f"Всегда пиши ответ пользователю"
            
        )
    payload = {
            "contents": [{"role": "user", "parts": [{"text": message_text}]}],
            "system_instruction": system_instruction,
            "tools": [UPDATE_KNOWLEDGE_TOOL]
        }
    result=await process_ai_function(payload=payload,context=context)
    await save_user_context(user_id, context)
    service_logger.info("%s пользователь, сообщение: %s, ответ: %s",user_id,message_text,result)
    return result

    