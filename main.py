from fastapi import FastAPI
import asyncio  # it is for async and awiat...  
app = FastAPI() # creating an instance of FastAPI application...

students=[
    {"id":1, "name": "jagan","age": 23},
    {"id":2, "name": "mohan","age": 24},
    {"id":3, "name": "joe","age":22 },
    {"id":4, "name": "asif","age":25 },
    {"id":5, "name": "ramesh","age":19 },
    {"id":6, "name": "venky","age": 23},
    {"id":7, "name": "raghu","age":15 }
]
staff=[
    {"id":1, "name": "jagaa","age": 23},
    {"id":2, "name": "mohan","age": 24},
    {"id":3, "name": "joe","age":22 },
    {"id":4, "name": "asif","age":25 },
    {"id":5, "name": "ramesh","age":19 },
    {"id":6, "name": "venky","age": 23},
    {"id":7, "name": "raghu","age":15 }
]

@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int):  # here we have to mention the data type (int/str/bool)
    for student in students:
        if student["id"] == student_id:
            return student
    # return f"{student['id']} this student is not found"
    return {"student not found"}

@app.get('/students/by-age/{stu_age}')
def get_stu_age(stu_age:int):
    names = [student['name'] for student in students if student["age"] > stu_age]
    return names


# async: Uesd to handle the tasks effeicently without blocking the application while for the something to finish...
# awiat: It wiats for the async opeartions to finish while allowing the event loop to handle the other work..

@app.get("/async")
async def async_():
    print(f"hi this is the main usage of the async...")

    await asyncio.sleep(5)
    print("this statement will print after 5 seconds in cmd..")

    return "hii.."

@app.get("/async/s_ages")
async def s_age():
    ages=[]
    for i in students :
        ages.append(i['age'])
    print(f"now the age will print after 2 seconds...")
    await asyncio.sleep(2)
    return ages

    # ages= [i['age'] for i in students]
    # return ages


@app.get("/async/await/wait")
async def awiat():
    await asyncio.sleep(3)
    print("this state will print after 3seconds using await..")
    await asyncio.sleep(3)
    return students

# Query parameters: It is a value pass through the URl...
# (http://127.0.0.1:8000/students?age=22)

# @app.get("/students/q_param/{age_param}")
# async def get_param(age_param:int):
#     params=[]
#     for i in students:
#         if i['age'] == age_param:
#             params.append(i)
#     return params

@app.get("/staff")
def get_all_staff():
    return staff
    
@app.get("/staff_list")
def get_staff(age:int):   # here we need to mention that var name and its data type...

    # if age is not None:
    #     res = [i for i in staff if i['age'] == age]
    #     return res

    res=[]
    for i in staff:
        if i['age'] == age: # query parameter for the age!!
            res.append(i)
    return res

@app.get("/staff_list/names")
def get_staff_names(name:str): # query parameter for the name!!
    res=[]
    for i in staff:
        if i['name'] == name:
            res.append(i)
    return res


# to run the file: uvicorn main:app --reload