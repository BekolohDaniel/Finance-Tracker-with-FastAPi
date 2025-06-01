from typing import Optional, List, Dict, Annotated

from fastapi import APIRouter, status, HTTPException, Query, Depends
from sqlmodel import select, func, and_

from database.authentication import SessionDep
from model.models import Category, Transaction, User
from schema.schemas import CategorySchema, CategoryRead, CategoryStats
from utils.oauth2 import get_current_user

category_route = APIRouter(
    prefix="/category",
    tags=['Category']
)


@category_route.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(category: Category, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    existing = session.exec(select(Category).where(Category.name == category.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(name=category.name.lower(), type=category.type)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category

@category_route.get("/", response_model=List[CategoryRead])
def get_categories(session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    return session.exec(select(Category)).all()

@category_route.get("/filter", response_model=List[CategoryRead])
def filter_cat_by_name(session:SessionDep,
                       current_user: Annotated[User, Depends(get_current_user)],
                       category_name:Optional[str] = Query(None)):

    query = select(Category)
    if category_name:
        query = query.where(Category.name == category_name)
    
    return session.exec(query).all()


@category_route.get("/stats", response_model=List[CategoryStats])
def get_category_stats(session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    categories = session.exec(select(Category)).all()
    for category in categories:
        total_amount = session.exec(
            select(func.sum(Transaction.amount))
            .where(and_(Transaction.category_id == category.id, Transaction.user_id == current_user.id))
        ).first() or 0

        print(f"Category: {category.name}, Total Amount: {total_amount}")
        
        transaction_count = session.exec(
            select(func.count(Transaction.id))
            .where(and_(Transaction.category_id == category.id, Transaction.user_id == current_user.id))
        ).first() or 0
        
        yield CategoryStats(category_name=category.name, total_amount=total_amount, transaction_count=transaction_count)


