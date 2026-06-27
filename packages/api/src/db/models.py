from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Float, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from shared.types.quotation import QuotationStatus

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    contact: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class Material(Base):
    __tablename__ = "materials"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    spec: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unit_price: Mapped[float] = mapped_column(Float)

class Draft(Base):
    __tablename__ = "drafts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    customer_name_raw: Mapped[str] = mapped_column(String)
    matched_customer_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("customers.id"), nullable=True)
    status: Mapped[QuotationStatus] = mapped_column(SQLEnum(QuotationStatus), default=QuotationStatus.DRAFT)
    matching_score: Mapped[float] = mapped_column(Float, default=0.0)
    needs_confirmation: Mapped[bool] = mapped_column(default=True)
    raw_data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    items: Mapped[List["DraftItem"]] = relationship("DraftItem", back_populates="draft", cascade="all, delete-orphan")

class DraftItem(Base):
    __tablename__ = "draft_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    draft_id: Mapped[str] = mapped_column(String, ForeignKey("drafts.id"))
    material_name_raw: Mapped[str] = mapped_column(String)
    matched_material_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("materials.id"), nullable=True)
    quantity: Mapped[float] = mapped_column(Float, default=1.0)
    unit_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    matching_score: Mapped[float] = mapped_column(Float, default=0.0)

    draft: Mapped["Draft"] = relationship("Draft", back_populates="items")
