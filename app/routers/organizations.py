from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from enum import Enum
import logging

from app import models
from app.database import engine, SessionLocal
from app.routers.auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)

models.Base.metadata.create_all(bind=engine)


class Organization(BaseModel):
    organization_ids: list[int] = Field(
        title=" ",
        description="Organizations IDs which have to be returned. By default - all organizations from apiLogin.\n\nCan be obtained by /api/1/organizations operation."
    )
    return_additional_info: bool = Field(
        title=" ",
        description="A sign whether additional information about the organization should be returned (RMS version, country, restaurantAddress, etc.), or only minimal information should be returned (id and name)."
    )
    include_disabled: bool = Field(
        title=" ", description="Attribute that shows that response contains disabled organizations."
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/",
             summary="Returns organizations available to api-login user.")
async def get_organizations_by_user(organization: Organization,
                                    user: dict = Depends(get_current_user),
                                    db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    # logging.warning(user.get("id"))

    return db.query(models.Organizations) \
        .filter(models.Organizations.owner_id == user.get("id")) \
        .filter(models.Organizations.id.in_(organization.organization_ids)) \
        .all()


def successful_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }


def http_exception():
    return HTTPException(status_code=404, detail="User not found")
