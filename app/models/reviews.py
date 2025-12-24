from sqlalchemy import ForeignKey, Text, Boolean, Integer, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    comment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    grade: Mapped[int] = mapped_column(Integer, CheckConstraint("grade >= 1 AND grade <= 5"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="reviews")
    product: Mapped["Product"] = relationship("Product", back_populates="reviews")
