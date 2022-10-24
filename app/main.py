from fastapi import FastAPI
from app import models
from app.database import engine

from app.routers import auth, todos, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
