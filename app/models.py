import enum

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum
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

    payment_types_owner = relationship("PaymentTypes", back_populates="organization")


class TerminalGroups(Base):
    __tablename__ = "terminal_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    timezone = Column(String)
    isAlive = Column(Boolean)

    organization_id = Column(Integer, ForeignKey("organizations.id"))

    terminal_groups_organization_owner = relationship("Organizations", back_populates="terminal_groups")

    payment_type_id = Column(Integer, ForeignKey("payment_types.id"))
    payment_type = relationship("PaymentTypes", back_populates="terminal_groups_owner")


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


class PaymentProcessingTypeEnum(str, enum.Enum):
    EXTERNAL = 'External'
    INTERNAL = 'Internal'
    BOTH = 'Both'


class PaymentTypeKindEnum(str, enum.Enum):
    UNKNOWN = 'Unknown'
    CASH = 'Cash'
    CARD = 'Card'
    CREDIT = 'Credit'
    WRITEOFF = 'Writeoff'
    VOUCHER = 'Voucher'
    EXTERNAL = 'External'
    IIKOCARD = 'Iikocard'


class PaymentTypes(Base):
    __tablename__ = "payment_types"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    name = Column(String)
    comment = Column(String)
    combinable = Column(Boolean)
    external_revision = Column(Integer)
    is_deleted = Column(Boolean)
    print_cheque = Column(Boolean)
    payment_processing_type: PaymentProcessingTypeEnum = Column(Enum(PaymentProcessingTypeEnum))
    payment_type_kind: PaymentTypeKindEnum = Column(Enum(PaymentTypeKindEnum))

    terminal_groups_owner = relationship("TerminalGroups", back_populates="payment_type")

    applicable_marketing_campaigns_owner = relationship("ApplicableMarketingCampaigns", back_populates="payment_type")

    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organizations", back_populates="payment_types_owner")


class ApplicableMarketingCampaigns(Base):
    __tablename__ = "applicable_marketing_campaigns"

    id = Column(Integer, primary_key=True, index=True)

    payment_type_id = Column(Integer, ForeignKey("payment_types.id"))
    payment_type = relationship("PaymentTypes", back_populates="applicable_marketing_campaigns_owner")
