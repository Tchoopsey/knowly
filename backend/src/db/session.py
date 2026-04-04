from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.core.config import DATABASE_URL

def get_db() -> Generator[Session, None, None]:
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

# DATABASE_URL = "sqlite+pysqlite:///./db/test.db"
# DATABASE_URL = "sqlite+pysqlite:///./:memory:"
# DATABASE_URL = "sqlite+pysqlite:///./db/knowly.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False},
)

LocalSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
