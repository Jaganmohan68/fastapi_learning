from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    field_validator,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .models import EmployeeDB

app = FastAPI(title="Employee API with PostgreSQL")

NonEmptyText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]


class EmployeeEmail(BaseModel):
    emp_email: EmailStr | None = None

    @field_validator("emp_email")
    @classmethod
    def validate_company_email(cls, value: EmailStr | None) -> EmailStr | None:
        if value is None:
            return value

        domain = str(value).rsplit("@", 1)[1].casefold()
        if domain != "mohan.com":
            raise ValueError("Email must use the @mohan.com company domain")

        return value


# Data the client must provide when creating or fully replacing an employee
class EmployeeData(EmployeeEmail):
    name: NonEmptyText
    department: NonEmptyText
    salary: int = Field(ge=0)
    location: NonEmptyText
    emp_email: EmailStr


# Data required to create an employee; the client supplies the ID
class EmployeeCreate(EmployeeData):
    employee_id: int = Field(gt=0)


# Data accepted when partially updating an employee
class EmployeePatch(EmployeeEmail):
    name: NonEmptyText | None = None
    department: NonEmptyText | None = None
    salary: int | None = Field(default=None, ge=0)
    location: NonEmptyText | None = None


# Fields the API sends back to the client
class EmployeeResponse(BaseModel):
    employee_id: int
    name: str
    department: str
    salary: int
    location: str | None = None
    emp_email: str | None = None
    model_config = ConfigDict(from_attributes=True)


# READ: return all employees
@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    statement = select(EmployeeDB)
    return db.scalars(statement).all()


# READ: return one employee by ID
@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.get(EmployeeDB, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return employee


# CREATE: add a new employee
@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(employee_data: EmployeeCreate, db: Session = Depends(get_db)):
    existing_employee = db.get(EmployeeDB, employee_data.employee_id)

    if existing_employee is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee ID already exists",
        )

    existing_email = db.scalar(
        select(EmployeeDB).where(EmployeeDB.emp_email == str(employee_data.emp_email))
    )
    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already assigned to an employee",
        )

    employee_values = employee_data.model_dump()
    employee_values["emp_email"] = str(employee_data.emp_email)
    employee = EmployeeDB(**employee_values)
    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


# UPDATE: replace all editable fields
@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def replace_employee(
    employee_id: int,
    employee_data: EmployeeData,
    db: Session = Depends(get_db),
):
    employee = db.get(EmployeeDB, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    existing_email = db.scalar(
        select(EmployeeDB).where(
            EmployeeDB.emp_email == str(employee_data.emp_email),
            EmployeeDB.employee_id != employee_id,
        )
    )
    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already assigned to another employee",
        )

    employee.name = employee_data.name
    employee.department = employee_data.department
    employee.salary = employee_data.salary
    employee.location = employee_data.location
    employee.emp_email = str(employee_data.emp_email)

    db.commit()
    db.refresh(employee)

    return employee


# UPDATE: change only the fields provided
@app.patch("/employees/{employee_id}", response_model=EmployeeResponse)
def patch_employee(
    employee_id: int,
    employee_data: EmployeePatch,
    db: Session = Depends(get_db),
):
    employee = db.get(EmployeeDB, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    changes = employee_data.model_dump(exclude_unset=True, exclude_none=True)

    if not changes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update",
        )

    if "emp_email" in changes:
        existing_email = db.scalar(
            select(EmployeeDB).where(
                EmployeeDB.emp_email == str(changes["emp_email"]),
                EmployeeDB.employee_id != employee_id,
            )
        )
        if existing_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already assigned to another employee",
            )
        changes["emp_email"] = str(changes["emp_email"])

    for field, value in changes.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)

    return employee


# DELETE: remove an employee by ID
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.get(EmployeeDB, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}
