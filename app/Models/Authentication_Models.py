from sqlmodel import SQLModel

class Token(SQLModel):
    token: str
    token_type: str

class TokenData(SQLModel):
    id: int | None = None