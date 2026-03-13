"""
Presentation of user data in MongoDB
"""
from pydantic import Field, BaseModel
from typing import Any

class MongoDBUserData(BaseModel):
    """
    Model that describes user data in MongoDB
    """
    core_objective:str=""
    user_data: dict={}
    ai_data: dict={}
    chat_history: list[dict[str,Any]]=[]


class MongoDBUser(BaseModel):
    """
    Model that describes user in MongoDB
    """
    id: int = Field(alias="_id")
    username: str | None = None
    user_data: MongoDBUserData = Field(default_factory=MongoDBUserData)

