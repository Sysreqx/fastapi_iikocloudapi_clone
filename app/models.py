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
    correlations = relationship("Correlations", back_populates="correlation_owner")


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todos")


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

    correlation_children = relationship("Correlations", back_populates="organization_parent")

    terminal_groups = relationship("TerminalGroups", back_populates="terminal_groups_organization_owner")

    order_types_children = relationship("OrderTypes", back_populates="organization")

    discounts_owner = relationship("Discounts", back_populates="organization")


class TerminalGroups(Base):
    __tablename__ = "terminal_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    timezone = Column(String)
    isAlive = Column(Boolean)
    # one to many
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    terminal_groups_organization_owner = relationship("Organizations", back_populates="terminal_groups")


class Correlations(Base):
    __tablename__ = "correlations"

    id = Column(Integer, primary_key=True, index=True)

    # children = relationship("Child", back_populates="parent")
    organization_children = relationship("CancelCauses", back_populates="correlation_parent")

    # parent_id = Column(Integer, ForeignKey("parent_table.id"))
    # parent = relationship("Parent", back_populates="children")
    organization_parent_id = Column(Integer, ForeignKey("organizations.id"))
    organization_parent = relationship("Organizations", back_populates="correlation_children")

    correlation_owner_id = Column(Integer, ForeignKey("users.id"))
    correlation_owner = relationship("Users", back_populates="correlations")


class CancelCauses(Base):
    __tablename__ = "cancel_causes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    is_deleted = Column(Boolean)

    # parent_id = Column(Integer, ForeignKey("parent_table.id"))
    # parent = relationship("Parent", back_populates="children")
    correlation_id = Column(Integer, ForeignKey("correlations.id"))
    correlation_parent = relationship("Correlations", back_populates="organization_children")


class OrderTypes(Base):
    __tablename__ = "order_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    orderServiceType = Column(String)
    isDeleted = Column(Boolean)
    externalRevision = Column(Integer)

    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organizations", back_populates="order_types_children")


class Discounts(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    percent = Column(Integer)
    isCategorisedDiscount = Column(Boolean)

    comment = Column(String)
    canBeAppliedSelectively = Column(Boolean)
    minOrderSum = Column(Integer)
    mode = Column(String)
    sum = Column(Integer)
    canApplyByCardNumber = Column(Boolean)
    isManual = Column(Boolean)
    isCard = Column(Boolean)
    isAutomatic = Column(Boolean)
    isDeleted = Column(Boolean)

    # productCategoryDiscounts in iiko
    categories_owner = relationship("Categories", back_populates="discount")

    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organizations", back_populates="discounts_owner")


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    percent = Column(Integer)

    discount_id = Column(Integer, ForeignKey("discounts.id"))
    discount = relationship("Discounts", back_populates="categories_owner")

