from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

from app import models
from app.database import engine, SessionLocal
from app.routers.auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/terminal_groups",
    tags=["Terminal groups"],
)

models.Base.metadata.create_all(bind=engine)


class TerminalGroup(BaseModel):
    organization_ids: list[int] = Field(
        title=" ",
        description="Organizations IDs for which information is requested.\n\nCan be obtained by /api/1/organizations operation."
    )
    return_additional_info: Optional[bool] = Field(
        title=" ",
        description="Attribute that shows that response contains disabled terminal groups.",
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/",
             summary="Method that returns information on groups of delivery terminals.")
async def get_organizations_by_user(terminal_group: TerminalGroup,
                                    user: dict = Depends(get_current_user),
                                    db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    # organizations = db.query(models.TerminalGroups).filter(models.TerminalGroups.owner_id == user.get("id")).all()

    return db.query(models.TerminalGroups)\
        .filter(models.TerminalGroups.organization_id.in_(terminal_group.organization_ids))\
        .all()


def successful_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }


def http_exception():
    return HTTPException(status_code=404, detail="User not found")
