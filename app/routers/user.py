
from fastapi import status, HTTPException, APIRouter

from .. import models, schemas, utils

from ..dependencies import db_dependency

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)




# create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: db_dependency):

    # Hash the password before saving to database
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# get users
@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: db_dependency):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found"
        )

    return user