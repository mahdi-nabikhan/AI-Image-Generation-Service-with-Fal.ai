from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from user.models import UserModel
from user.schemas import UserCreateResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserCreateResponse,
    status_code=201,
)
def create_user(
    db: Session = Depends(get_db),
):
    user = UserModel()

    db.add(user)
    db.commit()
    db.refresh(user)

    return user