from typing import Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app import models
from app.database import engine, SessionLocal
from app.routers.auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

models.Base.metadata.create_all(bind=engine)


class Order(BaseModel):
    id: int
    table_ids: list[int] = Field(
        title="Nullable",
        description="Table IDs."
    )


class CreateOrder(BaseModel):
    organization_id: int = Field(
        title=" ",
        description="Organization ID.\n\n"
                    "Can be obtained by /api/1/organizations operation."
    )
    terminal_group_id: int = Field(
        title=" ",
        description="Front group ID an order must be sent to.\n\n"
                    "Can be obtained by /api/1/organizations operation."
    )
    order: Order = Field(
        title=" ",
        description="Order."
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/",
             summary="Create order.",
             description="Allowed from version 7.4.6.\n\n"
                         "This method is a command. Use api/1/commands/status method to get the progress status.")
async def create_todo(order: CreateOrder,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    return successful_response(201)


def successful_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
