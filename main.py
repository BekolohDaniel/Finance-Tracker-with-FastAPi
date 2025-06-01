import os
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from database.authentication import create_db_and_tables
from router import user, login, transaction, category


@asynccontextmanager
async def lifespan(apps: FastAPI):
    # if os.path.exists("finance.db"):
    #     os.remove("finance.db")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def catch_all_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print("Unhandled error:", e)
        traceback.print_exc()
        raise e

app.include_router(user.user_route)
app.include_router(login.login_route)
app.include_router(transaction.transact_route)
app.include_router(category.category_route)



