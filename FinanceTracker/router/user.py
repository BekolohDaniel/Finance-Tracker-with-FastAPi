from typing import Annotated, List

from fastapi import APIRouter, Query, HTTPException, status, Depends
from sqlmodel import select

from database.authentication import SessionDep
from model.models import User
from schema.schemas import UserSchema, UpdateUserInfo
from utils.oauth2 import get_current_user
from utils.security import get_password_hash

user_route = APIRouter(
    prefix="/user",
    tags = ['User'],
)

@user_route.get("/", response_model=List[UserSchema])
def all_users(current_user: Annotated[User, Depends(get_current_user)],session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    users = session.exec(select(User).offset(offset).limit(limit)).all()

    return users

@user_route.post("/", response_model=UserSchema)
def new_user(session:SessionDep, user: User):
    users = session.exec(select(User).where(User.email == user.email)).first()
    if users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User exists already")

    hashed_password = get_password_hash(user.password)
    new_users = User(**user.model_dump())
    new_users.password = hashed_password

    session.add(new_users)
    session.commit()
    session.refresh(new_users)
    return UserSchema.model_validate(new_users)


@user_route.put("/edit", response_model=UserSchema)
def update_userinfo(update:UpdateUserInfo, session:SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    if current_user:
        current_user.email = update.email
        current_user.name = update.name

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user
