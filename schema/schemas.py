from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from model.models import TransactionType


class UserSchema(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UpdateUserPassword(BaseModel):
    password: str
    class Config:
        from_attributes = True


class UpdateUserInfo(BaseModel):
    name:str
    email:EmailStr


class TransactionSchema(BaseModel):
    amount: float
    description: str
    type: TransactionType
    timestamp: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

class UserTransaction(UserSchema):
    transaction: List[TransactionSchema]

    class Config:
        from_attributes = True

class CategorySchema(BaseModel):
    name: str
    type: TransactionType = TransactionType.expense
    transactions: List[TransactionSchema] = []
    class Config:
        from_attributes = True
        use_enum_values = True


class CategoryRead(CategorySchema):
    id: int

    class Config:
        from_attributes = True

class CategoryStats(BaseModel):
    category_name: str
    total_amount: float
    transaction_count: int

    class Config:
        from_attributes = True
        use_enum_values = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
