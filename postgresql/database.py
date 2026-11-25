from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="Jaganmohan@68",
    host="localhost",
    port=5432,
    database="fastapi_employees",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()