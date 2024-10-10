from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: str
    name: str
    email: Optional[str]
    location: Optional[str]
    joined_at: datetime
    preferences: Optional[dict]
    is_admin: Optional[bool] = False  