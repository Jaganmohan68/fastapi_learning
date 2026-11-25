from sqlalchemy import create_engine # this creates the sqlalchemy manager for the database.
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# sessionmaker: creates database session, which will use to read and write the records.
# declareative_base: gives us a base calss to defining database tables as python classes.

DATABASE_URL = "postgresql+psycopg://postgres:Jaganmohan@68@localhost:5432/fastapi_employees"
# DATABASE_URL: it containas host, dm_name, password, driver, port and username.

engine = create_engine(DATABASE_URL) # uses that url to connect to PostgreSQL

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) # It is factory for database sessions.

Base = declarative_base() # it is the parent class for our employee table.


from sqlalchemy import URL, create_engine

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="Jaganmohan@68",
    host="localhost",
    port=5432,
    database="fastapi_employees",
)

engine = create_engine(DATABASE_URL)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()