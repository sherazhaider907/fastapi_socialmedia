from jose import JWTError, jwt
from datetime import datetime, timedelta
#SECRET_KEY 

# using this  python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = "9ee639a218fa963d483506621be126e81091ca9ac1a3af7ca9021626ae15cd4e"

#ALGORITHM
ALGORITHM = "HS256"

#Expire time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
