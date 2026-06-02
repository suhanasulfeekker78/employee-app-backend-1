from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr
from pydantic import model_validator
from models.employee import EmployeeRole

from datetime import datetime


class CreateAddressInput(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Postal Code must contain only digits(0-9)")
        return v

    @model_validator(mode="after")
    def postal_code_length_for_country(self):
        country = self.country.strip().upper()
        n = len(self.postal_code)
        if country in ("US", "USA") and n != 5:
            raise ValueError("US ZIP codes must be exactly 5 digits")
        elif country == "IN" and n != 6:
            raise ValueError("Indian PIN codes must be exactly 6 digits")
        return self


class EmployeeAddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    line1: str
    city: str
    postal_code: str
    country: str


class EmployeeDepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class CreateEmployeeRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, extra="ignore"
    )  # extra='forbid'/'ignore'

    name: str = Field(min_length=1)
    email: EmailStr
    age: int | None = Field(ge=0, le=150)
    address: CreateAddressInput | None = None
    pswd: str = Field(min_length=6)
    role: EmployeeRole | None


class CreateEmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    age: int | None
    role: EmployeeRole


class UpdateEmployeeRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")
    name: str | None = Field(default=None, min_length=1)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=0, le=150)
    role: EmployeeRole | None = None


class GetEmployeeByIDResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    age: int | None
    role: str
    created_at: datetime
    updated_at: datetime | None
    addresses: list[EmployeeAddressResponse] = []
    departments: list[EmployeeDepartmentResponse] = []
