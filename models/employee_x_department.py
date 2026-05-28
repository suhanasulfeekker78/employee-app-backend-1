
from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from models.entity import Entity


class Employee_X_Department(Entity):

    __tablename__ = "employee_x_department"

    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("employee_id", "department_id"),
    )

