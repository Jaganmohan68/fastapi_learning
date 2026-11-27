from sqlalchemy import CheckConstraint, Column, Integer, String
from .database import Base


class EmployeeDB(Base):
    __tablename__ = "employees"
    __table_args__ = (
        CheckConstraint(
            "work_type IS NULL OR work_type IN ('remote', 'work_from_office')",
            name="ck_employees_work_type",
        ),
    )

    employee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    salary = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    emp_email = Column(String(254), nullable=True, unique=True, index=True)
    phone_number = Column(String(20), nullable=True)
    work_type = Column(String(30), nullable=True)
    