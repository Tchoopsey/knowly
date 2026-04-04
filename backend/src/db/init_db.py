import os
import shutil

from src.core.config import DATABASE_PATH, STORAGE_DIR
from .session import Base, engine
from .models import *
from .seed import seed

def init_db():
    print("Initializing new database and storage...\n")

    print("Starting cleanup...\n")
    if os.path.exists(DATABASE_PATH):
        print(f" - Removing {DATABASE_PATH}")
        os.remove(DATABASE_PATH)
        print(f" - {DATABASE_PATH} removed...")

    if os.path.exists(STORAGE_DIR):
        print(f" - Removing {STORAGE_DIR}")
        shutil.rmtree(STORAGE_DIR)
        print(f" - {STORAGE_DIR} removed...")

    print(f" - Creating new {STORAGE_DIR}")
    os.makedirs(STORAGE_DIR, exist_ok=True)
    
    print(f" - Creating new database {DATABASE_PATH}")
    Base.metadata.create_all(bind=engine)

    print("\nCleanup done...")

    print(f"\nStart seeding {DATABASE_PATH}\n")
    seed()

    print("Done.")

if __name__ == "__main__":
    init_db()
