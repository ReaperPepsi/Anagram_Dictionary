import jwt, yaml
from jwt import PyJWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.Models.Authentication_Models import Token, TokenData


oath2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

# use a dedicated part of the configuration file for token
with open("/Users/reaper_pepsi/Anagram_Dictionary/app/config/token_config_file.yaml", 'r') as config_file:
    config = yaml.full_load(config_file)


token_configuration = {
    "ALGORITHM": config['token']['ALGORITHM'],
    "SECRET_KEY": config['token']['SECRET_KEY'],
    "ACCESS_TOKEN_EXPIRE_MINUTES": config['token']['ACCESS_TOKEN_EXPIRE_MINUTES']
}



# create a JWT token for the user
def create_token_access(user_data: dict):
    payload = user_data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=token_configuration['ACCESS_TOKEN_EXPIRE_MINUTES'])
    payload.update({"exp": expire})

    encode_jwt = jwt.encode(payload, token_configuration['SECRET_KEY'], algorithm=token_configuration['ALGORITHM'])
    return encode_jwt



# verify the access token based on the payload data and based on the secret generated key
def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, token_configuration['SECRET_KEY'], algorithms=[token_configuration['ALGORITHM']])
        user_id: int = payload.get("user_id")

        if not user_id:
            raise credential_exception
        token_data = TokenData(id = user_id)

    except PyJWTError:
        raise credential_exception
    
    return token_data # -> token data will be used to get the current user id for session injection




def get_current_user(token: str = Depends(oath2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)