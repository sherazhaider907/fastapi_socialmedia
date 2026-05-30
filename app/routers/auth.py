from fastapi import APIRouter, HTTPException, status, Response

from ..dependencies import db_dependency

from .. import schemas , models , utils

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
    # return token
    return {"message": "Login successful"}
