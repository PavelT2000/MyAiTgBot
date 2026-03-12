from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class AIContext(BaseModel):
    core_objective: str = "Улучшить жизнь пользователя"
    persona_state: Dict[str, Any] = Field(default_factory=lambda: {
        "current_style": "Наблюдатель",
        "evolution_stage": 1
    })
    memory_bank: Dict[str, Any] = Field(default_factory=lambda: {
        "user_facts": [],
        "effective_triggers": [],
        "strategic_notes": ""
    })
    next_contact_time: Optional[str] = None
    is_waiting_contact: bool = False
    dynamic_data: Dict[str, Any] = Field(default_factory=dict)

class UserDocument(BaseModel):
    id: int = Field(alias="_id")
    username: str | None = None  # Здесь тоже добавь | None
    ai_context: AIContext = Field(default_factory=AIContext)