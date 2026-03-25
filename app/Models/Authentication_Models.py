from sqlmodel import SQLModel

class Token(SQLModel):
    token: str
    token_type: str

class Token_Data(SQLModel):
    id: int | None = None