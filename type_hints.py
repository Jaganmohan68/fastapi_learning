# type hints:   Type hints are used to tell python what type of data a varible, function parameter and function to have..
#               type hints are used to understand incoming data, validate it, convert it when possible and automatically generates swagger documention.


#example: 
#   without type hints:                
name = "jagan"
age = 21
is_active = True

# With type hints:

name:str = "jagan"  # we telling that varaible having "string" data type..
age:int = 21        ## we telling that varaible having "integer" data type..
is_active:bool = True   ## we telling that varaible having "boolean" data type..


# example program in function:
def add(a:int,b:int)-> int:  # here, function returns "int" value
    return a+b
res= add(2,3)
print(res)  



from fastapi import FastAPI

app = FastAPI()

@app.get("/student")

async def get_student(name: str, age: int) :

    return {
        "name": name,
        "age": age
    }
