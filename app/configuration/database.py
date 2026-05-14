from sqlmodel import SQLModel, create_engine, Session
from app.configuration.settings import settings

JOBS_DB_USER = settings.JOBS_DB_USER
JOBS_DB_PASSWORD = settings.JOBS_DB_PASSWORD
JOBS_DB_HOST = settings.JOBS_DB_HOST
JOBS_DB_PORT = settings.JOBS_DB_PORT
JOBS_DB_NAME = settings.JOBS_DB_NAME

DATABASE_URL = (
    f"mysql+pymysql://{JOBS_DB_USER}:{JOBS_DB_PASSWORD}"
    f"@{JOBS_DB_HOST}:{JOBS_DB_PORT}/{JOBS_DB_NAME}"
)

print(f"Connecting to database at {DATABASE_URL}")
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
