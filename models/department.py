from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.entity import Entity
from models.employee_x_department import Employee_X_Department


class Department(Entity):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    employees: Mapped[list["Employee"]] = relationship(  # noqa: F821
        "Employee",
        secondary=Employee_X_Department.__table__,
        back_populates="departments",
    )

    # def to_api_dict(self) -> dict[str, Any]:
    #     """JSON-friendly representation (ISO 8601 for timestamps)."""
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "created_at": datetime_to_iso(self.created_at),
    #         "updated_at": datetime_to_iso(self.updated_at),
    #         "deleted_at": datetime_to_iso(self.deleted_at)
    #     }
