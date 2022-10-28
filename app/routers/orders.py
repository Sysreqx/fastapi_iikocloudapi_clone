from enum import Enum
from typing import Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel, Field

from app import models
from app.database import engine, SessionLocal
from app.routers.auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

models.Base.metadata.create_all(bind=engine)


class GenderEnum(str, Enum):
    notspecified = 'NotSpecified'
    male = 'Male'
    female = 'Female'


class TypeEnum(str, Enum):
    regular = 'Regular'
    onetime = 'OneTime'


class Customer(BaseModel):
    name: str | None = None
    surname: str | None = None
    comment: str | None = None
    birthdate: date | None = None
    email: str | None = None
    should_receive_order_status_notifications: bool | None = None
    gender: GenderEnum = GenderEnum.notspecified
    type: TypeEnum = TypeEnum.onetime


class Order(BaseModel):
    external_number: str | None = None
    table_id: int | None = None
    customer: Customer | None = Field(
        title=" ",
        description="Guest.\n\n"
                    "Allowed from version 7.5.2."
    )
    phone: str | None = None
    guest_count: int | None = None
    guests: int | None = None
    # items array
    # combos array
    # payments array
    tab_name: int | None = None
    source_key: str | None = None
    order_type_id: str | None = None


class OrderSettings(BaseModel):
    transport_to_front_timeout: int | None = None


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
    create_order_settings: OrderSettings | None = Field(
        title=" ",
        description="Order creation parameters."
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
