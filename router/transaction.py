from datetime import date, datetime
from typing import List, Annotated, Optional

from fastapi import APIRouter, Depends, Query, HTTPException,status
from sqlalchemy import func
from sqlmodel import select, and_

from database.authentication import SessionDep
from model.models import Transaction, User, Category, TransactionType
from schema.schemas import TransactionSchema
from utils.oauth2 import get_current_user

import logging

logger = logging.getLogger("uvicorn.access")
logger.disabled = True

transact_route = APIRouter(
    prefix="/transaction",
    tags=['Transaction']
)

@transact_route.get("/by-month", response_model=List[TransactionSchema])
def group_transactions(
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000)
):
    try:
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid month or year")

    # Use the correct date field (assuming 'date' is the field in your model)
    statement = (
        select(Transaction)
        .where(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.timestamp >= start_date,
                Transaction.timestamp < end_date
            )
        )
        .order_by(Transaction.timestamp.desc())
    )

    results = session.exec(statement).all()
    return results


@transact_route.post("/new", response_model=TransactionSchema)
def create_transaction(
    transaction: TransactionSchema,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
):
    # Normalize description (category name)
    category_name = transaction.description.lower()

    # Look for category by name and type
    category = session.exec(
        select(Category).where(
            Category.name == category_name,
            Category.type == transaction.type,
        )
    ).first()

    # Create category if it doesn't exist
    if not category:
        category = Category(name=category_name, type=transaction.type)
        session.add(category)
        session.commit()
        session.refresh(category)

    new_transact = Transaction(
        user_id=current_user.id,
        category_id=category.id,
        amount=transaction.amount,
        description=transaction.description,
        type=transaction.type,
        timestamp=transaction.timestamp or datetime.now()
    )

    session.add(new_transact)
    session.commit()
    session.refresh(new_transact)
    return new_transact


@transact_route.get("/", response_model=List[Transaction])
def all_transact(session: SessionDep,
                    current_user: Annotated[User, Depends(get_current_user)],
                    offset: int = 0,
                    limit: Annotated[int, Query(le=100)] = 100
                    ):
    transact = session.exec(
        select(Transaction).where(Transaction.user_id == current_user.id).offset(offset).limit(limit)).all()

    return transact

@transact_route.get("/balance", response_model=float)
def get_balance(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
):
    total_income = session.exec(
        select(func.coalesce(func.sum(Transaction.amount), 0.0)).where(
            Transaction.user_id == current_user.id,
            Transaction.type == TransactionType.income
        )
    ).one()

    total_expense = session.exec(
        select(func.coalesce(func.sum(Transaction.amount), 0.0)).where(
            Transaction.user_id == current_user.id,
            Transaction.type == TransactionType.expense
        )
    ).one()

    balance = total_income - total_expense
    return balance


@transact_route.get("/{transact_id}", response_model=TransactionSchema)
def get_transaction(transact_id: int, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    transact = session.exec(
        select(Transaction)
        .where(Transaction.id == transact_id and Transaction.user_id == current_user.id)).first()

    if not transact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    return transact

@transact_route.delete("/{transact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transact_id: int, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    transact = session.exec(
        select(Transaction)
        .where(Transaction.id == transact_id and Transaction.user_id == current_user.id)).first()

    if not transact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )   
    session.delete(transact)
    session.commit()
    return {"detail": "Transaction deleted successfully"}