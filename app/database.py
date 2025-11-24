from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use absolute path for the SQLite DB to avoid differences depending on CWD
DB_PATH = Path(__file__).resolve().parent / "todos.db"
DATABASE_URL = f"sqlite:///{str(DB_PATH).replace('\\', '/')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    # Import models here so they are registered with Base.metadata
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
