from sqlmodel import SQLModel, Field

class User(SQLModel, table = True):
    __tablename__ = "users"
    user_id: int | None = Field(default = None, primary_key=True)
    username: str = Field( unique= True )
    password: str


# Schema for any new user that will create a login
class UserCreate(SQLModel):
    username: str
    password: str


# Schema response for the new created user
class UserResponse(SQLModel):
    username: str