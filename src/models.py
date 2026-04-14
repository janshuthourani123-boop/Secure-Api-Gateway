from pydantic import BaseModel, Field, field_validator
import re

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

class DataPayload(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)

    @field_validator('name', 'description')
    @classmethod
    def sanitize_input(cls, v: str | None) -> str | None:
        if v is None:
            return v
        forbidden_patterns = [r"<script.*?>", r"UNION SELECT", r"DROP\s+TABLE"]
        for pattern in forbidden_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Potentially malicious input detected")
        return v
