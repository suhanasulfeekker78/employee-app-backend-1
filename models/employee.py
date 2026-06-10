"""
Employee entity — ORM mapped class for table `employees`.
"""

from datetime import datetime
import enum

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum

from models.entity import Entity
from models.employee_x_department import Employee_X_Department


class EmployeeStatus(str, enum.Enum):
    PROBATION = "Probation"
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class EmployeeRole(str, enum.Enum):
    UI = "UI"
    UX = "UX"
    DEVELOPER = "Developer"
    HR = "HR"
    MANAGER = "Manager"


class Employee(Entity):
    __tablename__ = "employees"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
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

    status: Mapped[EmployeeStatus] = mapped_column(
        Enum(
            EmployeeStatus,
            name="employeestatus",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=True,
        server_default=EmployeeStatus.ACTIVE.value,
    )

    experience: Mapped[String] = mapped_column(String(20), nullable=True)

    joining_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    addresses: Mapped[list["Address"]] = relationship(  # noqa: F821
        "Address", back_populates="employee"
    )

    departments: Mapped[list["Department"]] = relationship(  # noqa: F821
        "Department",
        secondary=Employee_X_Department.__table__,
        back_populates="employees",
    )
