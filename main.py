import asyncio
from logger_config import setup_logging
from process_user_message import process_user_message

async def test_db():
    setup_logging()
    await process_user_message(123,"что тебе обо мне известно")
    
    
if __name__ == "__main__":
    asyncio.run(test_db())