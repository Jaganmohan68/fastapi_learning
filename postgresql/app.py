from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .models import EmployeeDB

app = FastAPI(title="Employee API with PostgreSQL")


# Data the client must provide when creating or fully replacing an employee
class EmployeeData(BaseModel):
    name: str
    department: str
    location: str


# Data required to create an employee; the client supplies the ID
class EmployeeCreate(EmployeeData):
    employee_id: int


# Data accepted when partially updating an employee
class EmployeePatch(BaseModel):
    name: str | None = None
    department: str | None = None
    location: str | None = None


# Fields the API sends back to the client
class EmployeeResponse(EmployeeData):
    employee_id: int
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

    employee = EmployeeDB(**employee_data.model_dump())
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

    employee.name = employee_data.name
    employee.department = employee_data.department
    employee.location = employee_data.location

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