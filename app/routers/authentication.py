from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.Models.User_Models import User
from app.utils.user_validation import validate_login
from app.utils.oath2 import create_token_access
from app.Models.Authentication_Models import Token
from app.Database.Postgres_connection_engine import SessionDep
from sqlmodel import select


router = APIRouter(
    tags = ['Authentication']
)


@router.post('/login', response_model=Token)
def login(session: SessionDep, user_credentials: OAuth2PasswordRequestForm = Depends()):
    user_from_db = session.exec(select(User).where(User.username == user_credentials.username)).first()

    if not user_from_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User does not exists")
    
    is_valid_user = validate_login(user_credentials.password, user_from_db.password)
    if not is_valid_user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials")
    
    # create an access token that will contain metadata PAYLOAD 
    access_token = create_token_access(user_data = {"user_id": user_from_db.user_id})
    return Token(token=access_token, token_type= "bearer")
    

