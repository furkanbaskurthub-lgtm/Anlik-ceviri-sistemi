from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(..., unique=True)
    password: str
    online_status: bool = False
    friends: List[str] = []  # List of usernames
    friend_requests: List[str] = []  # List of usernames who sent requests
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    preferred_language: str = "tr"  # Default language preference

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat() if dt else None
        } 