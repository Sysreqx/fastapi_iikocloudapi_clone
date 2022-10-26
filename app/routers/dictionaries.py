from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from enum import Enum
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
        description="Organizations IDs which have to be returned. By default - all organizations from apiLogin.\n\nCan be obtained by /api/1/organizations operation."
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

    query_correlations_id = db.query(models.Correlations.id)\
        .filter(models.Correlations.organization_parent_id.in_(organization.organization_ids))\
        .filter(models.Correlations.correlation_owner_id == user.get("id")) \
        .all()

    qci = []

    for i in query_correlations_id:
        emp_str = ""
        for m in str(i):
            if m.isdigit():
                emp_str = emp_str + m
        qci.append(int(emp_str))

    return db.query(models.CancelCauses) \
        .filter(models.CancelCauses.correlation_id.in_(qci)) \
        .all()


def successful_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }


def http_exception():
    return HTTPException(status_code=404, detail="User not found")
