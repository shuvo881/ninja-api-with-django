from datetime import date
from ninja import Schema, NinjaAPI
from .models import *



class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = 1
    birthdate: date = None

class EmployeeOut(EmployeeIn):
    cv: str = None
    id: int = None


