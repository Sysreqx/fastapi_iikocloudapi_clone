from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import logging

from app import models
from app.database import engine, SessionLocal
from app.routers.auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/dictionaries",
    tags=["Dictionaries"],
)

models.Base.metadata.create_all(bind=engine)


class Organization(BaseModel):
    organization_ids: list[int] = Field(
        title=" ",
        description="Organizations ids which delivery cancel causes needs to be returned.\n\nCan be obtained by /api/1/organizations operation."
    )


class OrganizationOrderTypes(BaseModel):
    organization_ids: list[int] = Field(
        title=" ",
        description="Organizations IDs which payment types have to be returned.\n\nCan be obtained by /api/1/organizations operation."
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/cancel_causes",
             summary="Delivery cancel causes.",
             description="Allowed from version 7.7.1.")
async def get_delivery_cancel_causes(organization: Organization,
                                     user: dict = Depends(get_current_user),
                                     db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    # logging.warning(user.get("id"))

    query_correlations_id = db.query(models.Correlations.id) \
        .filter(models.Correlations.organization_parent_id.in_(organization.organization_ids)) \
        .filter(models.Correlations.correlation_owner_id == user.get("id")) \
        .all()

    qci = []

    get_ids_from_list(query_correlations_id, qci)

    return db.query(models.CancelCauses) \
        .filter(models.CancelCauses.correlation_id.in_(qci)) \
        .all()


@router.post("/order_types",
             summary="Order types.")
async def get_payment_types(organization: OrganizationOrderTypes,
                            user: dict = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    list_ids = db.query(models.Organizations.id)\
        .filter(models.Organizations.owner_id == user.get("id"))\
        .filter(models.Organizations.id.in_(organization.organization_ids))\
        .all()

    logging.warning(list_ids)

    filtered_ids = []

    get_ids_from_list(list_ids, filtered_ids)

    return db.query(models.OrderTypes) \
        .filter(models.OrderTypes.organization_id.in_(filtered_ids)) \
        .all()


def successful_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }


def http_exception():
    return HTTPException(status_code=404, detail="User not found")


def get_ids_from_list(a_list, needed_list):
    for i in a_list:
        emp_str = ""
        for m in str(i):
            if m.isdigit():
                emp_str = emp_str + m
        needed_list.append(int(emp_str))
