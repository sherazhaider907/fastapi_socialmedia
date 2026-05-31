from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .dependencies import db_dependency
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#SECRET_KEY 

# using this  python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = "9ee639a218fa963d483506621be126e81091ca9ac1a3af7ca9021626ae15cd4e"

#ALGORITHM
ALGORITHM = "HS256"

#Expire time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(db: db_dependency,token: str = Depends(oauth2_scheme) ,):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user:
        raise credentials_exception
    return user