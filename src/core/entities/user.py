from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str | None = None
    email: EmailStr
    hashed_password: str
    role: Literal["admin", "user"] = "user"
    created_at: datetime = datetime.utcnow()
