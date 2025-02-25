from ninja import NinjaAPI, Schema
from ninja import UploadedFile, File
from django.core.files.storage import FileSystemStorage
from ninja.security import django_auth
from employees.api import *


api = NinjaAPI(csrf=True)

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
async def hello(request, data:HelloSchema):
    return f"Hello {data.name}, {request.user}"

# @api.get("/math")
# def math(request, a: int, b: int):
#     return {"add": a + b, "multiply": a * b}

@api.get("/math/{a}/{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}


class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str

class Error(Schema):
    message: str

@api.get("/me", response={200: UserSchema, 401: Error})
def me(request):
    if not request.user.is_authenticated:
        return 401, {"message": "Please sign in first"}
    return request.user 

@api.post("/employees", response={200: EmployeeOut, 400: Error})
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    employee = Employee.objects.create(**payload.dict())
    employee.cv.save(cv.name, cv)
    return employee


STORAGE = FileSystemStorage()

@api.post("/upload")
def create_upload(request, cv: UploadedFile = File(...)):
    filename = STORAGE.save(cv.name, cv)
    return {"name": filename, "url": STORAGE.url(filename)}

@api.get("/pets", auth=django_auth)
def pets(request):
    return f"Authenticated user {request.auth}"


from ninja.security import HttpBearer


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


@api.get("/bearer", auth=AuthBearer())
def bearer(request):
    return {"token": request.auth}

