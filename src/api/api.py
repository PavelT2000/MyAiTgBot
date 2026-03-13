from src.api.database import get_or_create_user
from src.api.context_maker import get_prompt_from_data
from src.api.ai_interface import answer_to_user_message
from src.api.models import MongoDBUser, AIRequest

async def process_user_message(user_id:int, message:str)->str:
    user: MongoDBUser=await get_or_create_user(tg_id=user_id, username=None)
    user.user_data.chat_history.append({
        "role":"user",
        "parts":[{
            "text":message
        }
        ]

    })
    prompt:AIRequest = await get_prompt_from_data(user.user_data)
    answer:str=await answer_to_user_message(prompt=prompt)
    user.user_data.chat_history.append({
        "role":"model",
        "parts":[{
            "text":answer
        }]
    })
    return answer

