from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class Part(BaseModel):
    text: Optional[str] = None
    inline_data: Optional[str] = None
    function_call: Optional[Any] = None  # Можно детализировать до модели
    function_response: Optional[Any] = None

class Content(BaseModel):
    role: str
    parts: List[Part]

class SafetySetting(BaseModel):
    category: str = Field(alias="additionalProp1")
    threshold: str = Field(alias="additionalProp2")

class Tool(BaseModel):
    # Дополнительные свойства инструментов обычно описываются через Dict
    function_declarations: Optional[List[Dict[str, Any]]] = Field(default=None, alias="additionalProp1")

class AIRequest(BaseModel):
    contents: List[Content]
    system_instruction: Optional[str] = None
    tools: Optional[List[Dict[str, Any]]] = None
    temperature: float = 0.7
    max_output_tokens: int = 1000
    top_p: float = 0.95
    top_k: int = 40
    safety_settings: Optional[List[Dict[str, str]]] = None