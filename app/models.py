from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship("Todos", back_populates="owner")
    operations = relationship("Operations", back_populates="operation_owner")
    organizations = relationship("Organizations", back_populates="organization_owner")

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todos")


# Notifications
class Operations(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    order_source = Column(String)
    order_id = Column(Integer)
    additional_info = Column(String)
    message_type = Column(String)
    organization_id = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    operation_owner = relationship("Users", back_populates="operations")


class Organizations(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    disabled = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))

    organization_owner = relationship("Users", back_populates="organizations")
    # many to one
    terminal_groups = relationship("TerminalGroups", back_populates="terminal_groups_organization_owner")


class TerminalGroups(Base):
    __tablename__ = "terminal_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Boolean)
    address = Column(Boolean)
    timezone = Column(Boolean)
    # one to many
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    terminal_groups_organization_owner = relationship("Organizations", back_populates="terminal_groups")

