from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select


from database.authentication import SessionDep
from model.models import User
from schema.schemas import Token
from utils.oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, ACCESS_TOKEN_EXPIRE_DAYS
from utils.security import verify_password

login_route = APIRouter(
    prefix="/login",
    tags = ['Login']
)

@login_route.post("/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],session: SessionDep):
    db_user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password. Try again")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )

    refresh_token = create_access_token(
        data={"sub": db_user.email, "refresh": True}, expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

