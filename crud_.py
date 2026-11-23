from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app =FastAPI()

employees={
    101:{
        "name":"jaga",
        "location":"vij",
        "dept":"cse"
    },
    102:{
            "name":"mohan",
            "location":"guntur",
             "dept":"IT"
        }
}


class EmployeeUpdate(BaseModel):
    name: str | None = None
    department: str | None = None
    location: str | None = None

# GET method

@app.get("/emp_details")
def get_employees():
    return employees

@app.get("/emp_details/{employees_id}")
def get_employees(employees_id:int):

    if employees_id in employees:
        return employees[employees_id]

    return {"message": "Employee not found"}


# POST method

class Employee(BaseModel):
    emp_id:int
    emp_name:str
    emp_location:str
    emp_dept:str

@app.post("/employees")
def create_employee(employee: Employee):

    if employee.emp_id in employees:
        return {"message": "Employee already exists"}

    employees[employee.emp_id] = {
        "name": employee.emp_name,
        "department": employee.emp_dept,
        "location": employee.emp_location
    }

    return {
        "message": "Employee created successfully",
        "employee_details": employees[employee.emp_id]
    }

# PUT method 

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):

    if employee_id not in employees:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    employees[employee_id] = {
        "name": employee.emp_name,
        "department": employee.emp_dept,
        "location": employee.emp_location
    }

    return {
        "message": "Employee updated successfully",
        "employee_details": employees[employee_id]
    }

#PATCH method:

@app.patch("/employees/{employee_id}")
def partially_update_employee(
    employee_id: int,
    employee: EmployeeUpdate
):

    if employee_id not in employees:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    update_data = employee.model_dump(exclude_unset=True)

    employees[employee_id].update(update_data)

    return {
        "message": "Employee partially updated successfully",
        "employee_details": employees[employee_id]
    }

#jagan
# #DELETE method

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id:int, employee: Employee):

    if employee_id not in employees:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

<<<<<<< HEAD
    deleted_employee= employees.pop(employee_id)
    return {
              f" employee deleted successfully: {deleted_employee}"
            }
=======
#     employees[employee_id] ={
        
#     }
>>>>>>> f8b9a18960ddf7646441dd6d337666a117ec8fde
