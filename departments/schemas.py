from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class DepartmentEmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str


class CreateDepartmentRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")
    name: str = Field(..., min_length=1, max_length=100)


class UpdateDepartmentRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")
    name: str = Field(..., min_length=1, max_length=100)


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    created_at: datetime
    updated_at: datetime | None


class DepartmentDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    created_at: datetime
    updated_at: datetime | None
    employees: list[DepartmentEmployeeResponse] = []
