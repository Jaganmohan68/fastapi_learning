from sqlalchemy import text

from .database import engine


def migrate():
    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE employees ADD COLUMN IF NOT EXISTS emp_email VARCHAR(254)")
        )
        connection.execute(
            text(
                "CREATE UNIQUE INDEX IF NOT EXISTS ix_employees_emp_email "
                "ON employees (emp_email)"
            )
        )

    print("The emp_email column and unique index are ready.")


if __name__ == "__main__":
    migrate()
