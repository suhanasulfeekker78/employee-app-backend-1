"""
Employee entity — ORM mapped class for table `employees`.
"""

from typing import Any

from sqlalchemy import  Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.entity import Entity, datetime_to_iso

class Employee(Entity):
    __tablename__ = "employees"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    
    addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="employees"
    )
    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": datetime_to_iso(self.created_at),
            "updated_at": datetime_to_iso(self.updated_at),
            "deleted_at": datetime_to_iso(self.deleted_at),
        }