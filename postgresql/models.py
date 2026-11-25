from sqlalchemy import Column, Integer, String
from .database import Base


class EmployeeDB(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)