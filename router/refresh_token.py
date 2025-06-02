from datetime import timedelta

import jwt
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import select

from database.authentication import SessionDep
from model.models import User
from schema.schemas import Token
from utils.oauth2 import SECRET_KEY, ALGORITHM, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, \
    ACCESS_TOKEN_EXPIRE_DAYS

refresh_route = APIRouter(
    prefix="/refresh",
    tags=["Auth"]
)

@refresh_route.post("/", response_model=Token)
async def refresh_access_token(
    refresh_token: str = Body(..., embed=True),
    session: SessionDep = Depends()
):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        is_refresh = payload.get("refresh", False)

        if not email or not is_refresh:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    new_refresh_token = create_access_token(
        data={"sub": email, "refresh": True},
        expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    )

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )