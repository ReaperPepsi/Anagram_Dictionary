from app.Models.User_Models import User, UserCreate, UserResponse
from app.Database.Postgres_connection_engine import SessionDep
from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from app.utils.user_validation import password_hasher

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate ,session: SessionDep):
    check_existing_user = session.exec(select(User).where(User.username == user.username)).first()

    if check_existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user.password = password_hasher(user.password)
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

