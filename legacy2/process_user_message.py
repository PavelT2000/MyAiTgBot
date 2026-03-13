"""
Module that proccess user interactions
"""
import logging
from tools import UPDATE_KNOWLEDGE_TOOL, SCHEDULE_REMINDER_TOOL
from database import get_or_create_user, save_user_context
from embedding import get_relevant_facts
from process_ai_function import process_ai_function



service_logger=logging.getLogger('service')


async def process_user_message(user_id: int, message_text: str) -> str:
    """
    Function of processing user message
    """
    user_doc = await get_or_create_user(user_id)
    context = user_doc.ai_context
    # 1. Поиск фактов (RAG)
    relevant_facts = await get_relevant_facts(
        context.memory_bank.get('user_facts', []),
        message_text, n=100
        )
    facts_strings = [f"- {f['text']} [{f.get('category', 'общие')}]" for f in relevant_facts]
    # 2. Подготовка истории (берем последние 10 сообщений)
    # Если chat_history еще нет (None), создаем пустой список
    if not hasattr(context, 'chat_history') or context.chat_history is None:
        context.chat_history = []
    short_history = context.chat_history[-10:]

    system_instruction = (
        f"Твоя цель: Сделать жизнь пользователя лучше, вести себя подобно человеку. "
        f"Факты о пользователе: {'\n'.join(facts_strings) or 'Нет данных.'}. "
        f"Заметки: {context.memory_bank.get('strategic_notes', '')}. "
        """
        КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО:
        Писать свои мысли, планы или варианты ответов.
        Использовать заголовки, списки или технический анализ.
        Выдавать что-либо, кроме прямой речи, обращенной к человеку.
        Пиши сразу результат.
        """
    )

    # 3. Формируем текущее сообщение пользователя
    user_message = {"role": "user", "parts": [{"text": message_text}]}

    # 4. Собираем payload, включая историю
    payload = {
        # История + новое сообщение пользователя
        "contents": short_history + [user_message], 
        "system_instruction": system_instruction,
        "tools": [UPDATE_KNOWLEDGE_TOOL, SCHEDULE_REMINDER_TOOL]
    }

    # ПЕРВЫЙ ВЫЗОВ
    answer, was_function_called = await process_ai_function(payload, context, user_id=user_id)

    # ВТОРОЙ ВЫЗОВ (если была функция)
    if was_function_called:
        if not answer or len(answer.strip()) < 5:
            service_logger.info("ИИ вызвал функцию молча, запрашиваем комментарий...")
            # Добавляем в историю техническое сообщение о том, что база обновлена
            # Это "сигнал" для ИИ, что его команда выполнена
            context.chat_history.append(user_message)
            context.chat_history.append({
                "role": "model", 
                "parts":
                    [{"text": "Я сохранил данные в базу знаний. Надо что-то сказать пользователю"}]
            })
            # Обновляем payload (уже без tools, чтобы не зациклиться)
            new_payload = {
                "contents": context.chat_history[-10:],
                "system_instruction": system_instruction
            }
            # Запрашиваем финальный текст
            answer, _ = await process_ai_function(new_payload, context,user_id=user_id)
        else:
            # ИИ уже всё сказал ("Ок, через минуту напишу!"), просто идем дальше
            service_logger.info("ИИ выдал ответ вместе с вызовом функции: %s", answer)
    else:
        # Если функций не было, просто сохраняем текущий диалог
        context.chat_history.append(user_message)
        context.chat_history.append({"role": "model", "parts": [{"text": answer}]})

    answer = clean_ai_answer(answer)
    # 6. СОХРАНЕНИЕ В ИСТОРИЮ
    # Добавляем сообщение пользователя
    if not was_function_called:
        context.chat_history.append(user_message)
    # Добавляем ответ ИИ
    context.chat_history.append({"role": "model", "parts": [{"text": answer}]})

    # Ограничиваем общую длину истории в БД (например, последние 50 сообщений),
    # # чтобы документ в MongoDB не рос бесконечно
    context.chat_history = context.chat_history[-50:]

    # 7. Сохраняем обновленный контекст в БД
    await save_user_context(user_id, context)
    service_logger.info("%s пользователь, сообщение: %s, ответ: %s", user_id, message_text, answer)
    return answer


def clean_ai_answer(text: str) -> str:
    """
    Clean answer of ai from thinking
    """
    # 1. Если модель пишет "Финальный ответ:" или "Выбранный ответ:"
    markers = ["Финальный ответ:", "Выбранный ответ:", "### Ответ"]
    for marker in markers:
        if marker in text:
            text = text.split(marker)[-1]

    # 2. Если модель выдает огромный блок рассуждений,
    # ответ обычно идет в самом последнем абзаце.
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    if len(paragraphs) > 3: # Если абзацев подозрительно много
        # Берем последний абзац, если он похож на прямую речь
        return paragraphs[-1].strip('"')
    return text.strip().strip('"')
