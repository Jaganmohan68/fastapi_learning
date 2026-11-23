from fastapi import FastAPI
from pydantic import BaseModel # Importing base model to define and validate data structures...

app= FastAPI()

class Student_details(BaseModel): # defining student model using Pydantic
    name: str # the student's name must be a string
    age: int # the student's age must be a integer
    email: str # the student's email must be a string

class Student_full_details(BaseModel):
    ph_no: int
    address:str
    parent_ph:int

class First_name(BaseModel):
    f_name:str

class last_name(BaseModel):
    l_name: str

@app.post("/stu_data")
def create_student(student: Student_details):
    return f"student created successfully{student}"

@app.post("/stu_data/full_data")
def adding_full_details(student:Student_full_details):
    return f"now adding full details of the student...{student}"

@app.post("/stu_data/L_name")
def add_last_name(student: last_name):
    return f"student added her/his last name successfully {student}"

# @app.get("/stu_data")
# def stu_data():
#     return stu_data

@app.post("/")
def f_name(f_name:First_name):
    return f"hi {f_name}"
    