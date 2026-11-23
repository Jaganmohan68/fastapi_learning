# starlette:    it is lightweight framework for building asyncronus web applications...
#               FastAPI uses starlette internally, then fastapi may adds additional features..
#               FastAPI builds on starletter...
#features of starlette:
#                   - middleware: It acts like a security checkpoint b/w client and our application...
#                   - requests: It represents the info sent by the client to the server..
#                               starlette provides "request" object to access details of (POSTMAN)..
#                   - response: When client send the requests from the client, then server get the response from the server..
#                   - routing: whatever the request you got from the client, that request will be sent to the correct API (becoz the rounting)..




# startlatte--middleware: 


from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def my_middleware(request: Request, call_next):

    print("Request received")

    start_time = time.time()

    # Send request to the endpoint
    response = await call_next(request)

    # Calculate processing time
    process_time = time.time() - start_time

    response.headers["X-Process-Time"] = str(process_time)

    print("Response generated")

    return response


@app.get("/middleware")
async def home():
    return {"Vanakkam🙌"}


#starlette_request: A request object contains the information about the http request...

@app.get("/staff")
async def get_staff(request: Request):

    staff_name = request.query_params.get("name")

    return {
        "name": staff_name,
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers)
    }

#starlatte_response: 
@app.get("/student")

async def get_staff():

    return JSONResponse(
        content={
            "name": "Joe",
            "department": "IT",
            "status": "Active"
        },
        status_code=200
    )


#starlatte_routing: process of redircting an incoming http request to the appropriate endpioint on its url and http method

# GET route
@app.get("/staff")
async def get_staff():
    return {"message": "All staff details"}

# POST route
@app.post("/staff")
async def create_staff():
    return {"message": "Staff created"}

# GET route with path parameter
@app.get("/staff/{staff_id}")
async def get_staff_by_id(staff_id: int):
    return {

        "staff_id": staff_id,
        "name": "Joe"
    }

# PUT route
@app.put("/staff/{staff_id}")
async def update_staff(staff_id: int):
    return {
        "message": "Staff updated",
        "staff_id": staff_id
    }

# DELETE route
@app.delete("/staff/{staff_id}")
async def delete_staff(staff_id: int):
    return {
        "message": "Staff deleted",
        "staff_id": staff_id
    }