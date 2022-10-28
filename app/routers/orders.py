import logging
from enum import Enum
from typing import List

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


class ItemTypeEnum(str, Enum):
    product = 'Product'
    compound = 'Compound'


class ComboInformation(BaseModel):
    combo_id: int
    combo_source_id: int
    combo_group_id: int


class Item(BaseModel):
    id: int
    price: int | None = None
    positionId: int | None = None
    type: ItemTypeEnum = ItemTypeEnum.product
    amount: int
    productSizeId: int
    combo_information: ComboInformation | None
    comment: str | None = None


class PaymentsTypeKindEnum(str, Enum):
    CASH = 'Cash'
    CARD = 'Card'
    IIKOCARD = 'Iikocard'
    EXTERNAL = 'External'


class Payment(BaseModel):
    payment_type_kind: PaymentsTypeKindEnum = PaymentsTypeKindEnum.CASH
    sum: int
    payment_type_id: int
    is_processed_externally: bool | None = None
    is_fiscalized_externally: bool | None = None


class Combo(BaseModel):
    id: int
    name: str
    amount: int
    price: int
    sourceId: int
    programId: int | None = None


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
    items: List[Item] = Field(
        title=" ",
        description="Order items."
    )
    combos: List[Combo] | None = Field(
        title=" ",
        description="Combos included in order."
    )
    payments: List[Payment] | None = Field(
        title=" ",
        description="Order payment components."
    )
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


class GetOrderById(BaseModel):
    source_keys: list[int] | None = Field(
        title=" ",
        description="Source keys."
    )
    organization_ids: list[int] = Field(
        title=" ",
        description="Organization IDs.\n\n"
                    "Can be obtained by /api/1/organizations operation."
    )
    order_ids: list[int] | None = Field(
        title=" ",
        description="Order IDs.\n\n"
                    "Required if \"orderIds\" is null. Must be null if \"orderIds\" is not null."
    )
    pos_order_ids: list[int] | None = Field(
        title=" ",
        description="Order IDs.\n\n"
                    "Required if \"orderIds\" is null. Must be null if \"orderIds\" is not null."
    )


class AddCustomerToOrder(BaseModel):
    organization_id: int = Field(
        title=" ",
        description="Organization ID.\n\n"
                    "Can be obtained by /api/1/organizations operation."
    )
    order_id: int = Field(
        title=" ",
        description="Order ID."
    )
    customer: Customer = Field(
        title=" ",
        description="Guest info."
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
async def create_order(order: CreateOrder,
                       user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    list_ids = db.query(models.Organizations.id) \
        .filter(models.Organizations.owner_id == user.get("id")) \
        .filter(models.Organizations.id.in_([order.organization_id])) \
        .all()
    organization_ids = []
    get_ids_from_list(list_ids, organization_ids)

    if order.organization_id not in organization_ids:
        raise HTTPException(status_code=404, detail="Organization not found")

    order_model = models.Orders()

    order_model.external_number = order.order.external_number
    order_model.table_id = order.order.table_id
    order_model.phone = order.order.phone
    order_model.guest_count = order.order.guest_count
    order_model.guests = order.order.guests
    order_model.tab_name = order.order.tab_name
    order_model.source_key = order.order.source_key
    order_model.order_type_id = order.order.order_type_id
    order_model.organization_id = order.organization_id

    db.add(order_model)
    db.commit()

    return successful_response(201)


@router.post("/order_id/",
             summary="Retrieve orders by IDs.",
             description="Allowed from version 7.4.6.")
async def get_orders_by_ids(order: GetOrderById,
                            user: dict = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    list_ids = db.query(models.Organizations.id) \
        .filter(models.Organizations.owner_id == user.get("id")) \
        .filter(models.Organizations.id.in_(order.organization_ids)) \
        .all()
    organization_ids = []
    get_ids_from_list(list_ids, organization_ids)

    logging.warning(organization_ids)

    if not organization_ids:
        raise HTTPException(status_code=404, detail="Organization not found")

    order_model = db.query(models.Orders) \
        .filter(models.Orders.organization_id.in_(organization_ids)) \
        .filter(models.Orders.id.in_(order.order_ids)) \
        .all()

    if not order_model:
        return http_exception()

    return order_model


@router.post("/add_customer/",
             summary="Add customer to order.",
             description="Allowed from version 7.7.1.\n\n"
                         "This method is a command. Use api/1/commands/status method to get the progress status.")
async def add_customer(order: AddCustomerToOrder,
                       user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    list_ids = db.query(models.Organizations.id) \
        .filter(models.Organizations.owner_id == user.get("id")) \
        .filter(models.Organizations.id.in_([order.organization_id])) \
        .all()
    organization_ids = []
    get_ids_from_list(list_ids, organization_ids)

    if order.organization_id not in organization_ids:
        raise HTTPException(status_code=404, detail="Organization not found")

    order_model = db.query(models.Orders) \
        .filter(models.Orders.id == order.order_id) \
        .first()

    if order_model is None:
        return http_exception()

    customer_model = db.query(models.Customers) \
        .filter(models.Customers.email == order.customer.email) \
        .first()

    if customer_model is None:
        customer_model = models.Customers()

        customer_model.name = order.customer.name
        customer_model.surname = order.customer.surname
        customer_model.comment = order.customer.comment
        customer_model.birthdate = order.customer.birthdate
        customer_model.email = order.customer.email
        customer_model.should_receive_order_status_notifications = order.customer.should_receive_order_status_notifications
        customer_model.gender = order.customer.gender
        customer_model.type = order.customer.type

        db.add(customer_model)
        db.commit()

        customer_model = db.query(models.Customers) \
            .filter(models.Customers.email == order.customer.email) \
            .first()

    order_model.customer_id = customer_model.id
    db.add(order_model)
    db.commit()

    return successful_response(201)


def successful_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }


def http_exception():
    return HTTPException(status_code=404, detail="Order not found")


def get_ids_from_list(a_list, needed_list):
    for i in a_list:
        emp_str = ""
        for m in str(i):
            if m.isdigit():
                emp_str = emp_str + m
        needed_list.append(int(emp_str))
