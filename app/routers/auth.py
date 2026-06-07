from fastapi import APIRouter, HTTPException, status, Response , Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..dependencies import db_dependency

from .. import schemas , models , utils , oauth2

router = APIRouter(
    tags=["Authentication"],
)

@router.post("/login",response_model=schemas.Token)
async def login(db: db_dependency ,user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return token
    return {"access_token": access_token, "token_type": "bearer"}
