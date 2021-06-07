from typing import List
from fastapi import HTTPException, APIRouter
from ..database import database_connection
from ..models import *
from ..schemas import *

router = APIRouter(prefix='/api/v1/users')

# ---------------Users---------------

@router.post('', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, "Este nombre de usuario ya existe")

    hash_password = User.create_password(user.password)

    # Creating new user in  DB
    user = User.create(
        username = user.username,
        password = hash_password
    )

    return UserResponseModel(id=user.id, username=user.username)

@router.get('', response_model=List[UserResponseModel])
async def get_users():
    users = User.select()

    return [user for user in users]


