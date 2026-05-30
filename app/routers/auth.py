from fastapi import APIRouter, HTTPException, status, Response

from ..dependencies import db_dependency

from .. import schemas , models , utils , oauth2

router = APIRouter(
    tags=["Authentication"],
)

@router.post("/login")
async def login(user_credentials: schemas.UserLogin, db: db_dependency):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return token
    return {"access_token": access_token, "token_type": "bearer"}
