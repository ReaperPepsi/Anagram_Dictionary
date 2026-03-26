from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.Models.User_Models import User, UserCreate, UserResponse
from app.utils.user_validation import validate_login
from app.utils.oath2 import create_token_access
from app.Models.Authentication_Models import Token
from app.Database.Postgres_connection_engine import SessionDep
from sqlmodel import select
from app.utils.user_validation import password_hasher
from app.logging_config import logger


router = APIRouter(
    prefix = "/auth",
    tags = ['Authentication']
)

log = logger.getChild("auth")


@router.post('/login', response_model=Token)
def login(session: SessionDep, user_credentials: OAuth2PasswordRequestForm = Depends()):
    user_from_db = session.exec(select(User).where(User.username == user_credentials.username)).first()

    if not user_from_db:
        log.warning(f"Login failed for: {user_credentials.username} - does not exists inside database")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User does not exists")
    
    is_valid_user = validate_login(user_credentials.password, user_from_db.password)
    if not is_valid_user:
        log.warning(f"Login failed for: {user_credentials.username} - wrong password")
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials")
    
    # create an access token that will contain metadata PAYLOAD 
    access_token = create_token_access(user_data = {"user_id": user_from_db.user_id})
    return Token(token=access_token, token_type= "bearer")
    



@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate ,session: SessionDep):
    check_existing_user = session.exec(select(User).where(User.username == user.username)).first()

    if check_existing_user:
        log.warning(f"Create a new login failed - {user.username} already exists")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user.password = password_hasher(user.password)
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user
