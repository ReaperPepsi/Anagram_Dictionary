from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Index, UniqueConstraint
from sqlalchemy.sql import func
from datetime import datetime
from typing import List

# Dictionary Table
class AnagramDictionary(SQLModel, table = True):
    __tablename__ = 'Dictionary'
    id: int | None = Field(default = None, primary_key = True)
    key_word: str
    word: str
    user_id: int = Field(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("users.user_id", ondelete="CASCADE"),
            nullable=False
        )
    )
    created_at: datetime | None = Field(
        default = None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now()
        )
    )

    __table_args__ = (
    UniqueConstraint("user_id", "word", name="uq_user_word"),
    Index("idx_user_key", "user_id", "key_word")
)
    

# User input list of words to be grouped
class AnagramsInput(SQLModel):
    words: list[str]

# Response based on the client input
class AnagramPostResponse(SQLModel):
    added: list[str] | None
    skipped: list | None

# Schema for list endpoint for grouping the corresponding words
class AnagramGroup(SQLModel):
    key_word: str
    words: List[str] = Field(default_factory=list)

# Schema for list endpoint response
class AllAnagramGroupsResponse(SQLModel):
    groups: List[AnagramGroup] = Field(default_factory=list)

