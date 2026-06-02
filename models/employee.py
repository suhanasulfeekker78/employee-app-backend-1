"""
Employee entity — ORM mapped class for table `employees`.
"""

import enum

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum

from models.entity import Entity
from models.employee_x_department import Employee_X_Department


class EmployeeRole(str, enum.Enum):
    UI = "UI"
    UX = "UX"
    DEVELOPER = "Developer"
    HR = "HR"


class Employee(Entity):
    __tablename__ = "employees"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[EmployeeRole] = mapped_column(
        Enum(
            EmployeeRole,
            name="employeerole",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        server_default=EmployeeRole.DEVELOPER.value,
    )

    addresses: Mapped[list["Address"]] = relationship(  # noqa: F821
        "Address", back_populates="employee"
    )

    @property
    def active_addresses(self) -> list["Address"]:  # noqa: F821
        return [a for a in self.addresses if a.deleted_at is None]

    departments: Mapped[list["Department"]] = relationship(  # noqa: F821
        "Department",
        secondary=Employee_X_Department.__table__,
        back_populates="employees",
    )
