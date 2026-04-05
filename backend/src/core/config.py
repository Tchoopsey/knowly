import os
from pathlib import Path


BASE_DIR = Path(os.getenv("KNOWLY_BASE_DIR", Path(__file__).resolve().parents[3]))

DATA_DIR = (BASE_DIR / "data").resolve()
DATABASE_DIR = (DATA_DIR / "db").resolve()
STORAGE_DIR = (DATA_DIR / "storage/documents").resolve()
STORAGE_BAK_DIR = (BASE_DIR / "storage_bak/documents/team_1").resolve()

DATABASE_PATH = (DATABASE_DIR / "test.db").resolve()
DATABASE_URL = f"sqlite+pysqlite:///{DATABASE_PATH}"
