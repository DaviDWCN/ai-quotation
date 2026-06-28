from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from packages.shared.types.quotation import DraftStatus

class Base(DeclarativeBase):
    pass

class CustomerModel(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    contact: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class MaterialModel(Base):
    __tablename__ = "materials"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    specification: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unit_price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class DraftModel(Base):
    __tablename__ = "drafts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    customer_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("customers.id"), nullable=True)
    customer_match_score: Mapped[float] = mapped_column(Float, default=0.0)
    customer_candidates: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)

    parsed_data: Mapped[Dict[str, Any]] = mapped_column(JSON)
    material_matches: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)

    status: Mapped[DraftStatus] = mapped_column(SQLEnum(DraftStatus), default=DraftStatus.DRAFT)
    needs_confirmation: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
