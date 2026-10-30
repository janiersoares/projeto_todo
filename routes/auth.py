from fastapi import APIRouter, Depends, HTTPException

from db import get_connection
from repositories.user_repository import UserRepository
from schemas.user import UserCreate, UserOut
from services.user_service import EmailAlreadyRegistered, UserService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service(connection=Depends(get_connection)):
    return UserService(UserRepository(connection))


@router.post("/register", status_code=201, response_model=UserOut)
def register(body: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        user = service.register(body.email, body.password)
    except EmailAlreadyRegistered:
        raise HTTPException(status_code=409, detail="Email already registered")

    return UserOut(
        id=user["id"],
        email=user["email"],
        created_at=user["created_at"].isoformat(),
    )