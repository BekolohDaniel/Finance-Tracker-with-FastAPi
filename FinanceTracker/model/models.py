from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List

from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str = Field(index=True)

    transactions: List["Transaction"] =  Relationship(back_populates="user")


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    type: str = Field(default=TransactionType)

    transactions: List["Transaction"] = Relationship(back_populates="category")

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    category_id: Optional[int] = Field(foreign_key="category.id")
    amount: float
    description: str
    type: TransactionType = Field(default=TransactionType.expense)
    timestamp: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    user: Optional[User] = Relationship(back_populates="transactions")
    category: Optional[Category] = Relationship(back_populates="transactions")





