import httpx
from src.api.models import AIRequest
from src.config import config
async def answer_to_user_message(prompt:AIRequest)->str:
    """
    procesing function of ai
    """
    async with httpx.AsyncClient(trust_env=False) as client:
        print("🚀 Запрос на прокси: %s", config.api_chat_url)
        response = await client.post(
            config.api_chat_url,
            json=prompt.model_dump(by_alias=True, exclude_none=True),
            timeout=30.0)
        response.raise_for_status()
        result = response.json()
    return result.get('answer', '')

