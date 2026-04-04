import os
import glob
import shutil
from uuid import uuid4

from src.core.config import STORAGE_BAK_DIR, STORAGE_DIR
from src.core.security import hash_password

from .models import Document, Team, User, UserRole
from .session import LocalSession

def seed():
    with LocalSession() as db:
        print(" - Creating teams...")
        print(" - Creating first team...")
        team_id = str(uuid4())
        team_path = os.path.join(STORAGE_DIR, f"team_{team_id}")
        team = Team(
            id=team_id,
            team_name="First Team",
            team_path=team_path
        )
        print(f"\t{team.team_name} created...")
        print(f"\tDirectory path: {team.team_path}")

        print(" - Creating Admin team...")
        admin_team_id = str(uuid4())
        admin_team_path = os.path.join(STORAGE_DIR, f"team_{admin_team_id}")
        admin_team = Team(
            id=admin_team_id,
            team_name="Admin Team",
            team_path=admin_team_path
        )
        print(f"\t{admin_team.team_name} created...")
        print(f"\tDirectory path: {admin_team.team_path}")

        print(" - Creating directories for teams...")
        os.makedirs(team.team_path, exist_ok=True)
        print(f"\t'{team.team_name}': '{team.team_path}'")
        os.makedirs(admin_team.team_path, exist_ok=True)
        print(f"\t'{admin_team.team_name}': '{admin_team.team_path}'")

        print(f" - Reseeding files for '{team.team_name}' from '{STORAGE_BAK_DIR}' to '{team.team_path}'")
        for file_path in glob.glob(os.path.join(STORAGE_BAK_DIR, "*")):
            if os.path.isfile(file_path):
                print(f" - Copying file '{file_path}' to '{team.team_path}'")
                shutil.copy(file_path, team.team_path)


        print(" - Adding teams to the database...")
        db.add_all([team, admin_team])
        db.flush()

        print(" - Creating users...")
        print(" - Creating admin user...")
        hash_admin = hash_password("deki123")
        admin = User(
            id=str(uuid4()),
            team_id=admin_team_id,
            first_name="Dejan",
            last_name="Samardzic",
            email="ds@email.com",
            username="dekis",
            password=hash_admin,
            role=UserRole.ADMIN,
        )
        print(f"\tAdmin user '{admin.username}' created...")

        print(" - Creating lead user...")
        hash_lead = hash_password("zoki123")
        lead = User(
            id=str(uuid4()),
            team_id=team_id,
            first_name="Zoran",
            last_name="Mamdani",
            email="zoks69@email.com",
            username="zoks69",
            password=hash_lead,
            role=UserRole.TEAM_LEAD,
        )
        print(f"\tLead user '{lead.username}' created...")

        print(" - Creating worker user...")
        hash_worker = hash_password("baja123")
        worker = User(
            id=str(uuid4()),
            team_id=team_id,
            first_name="Baja",
            last_name="Malic",
            email="baja@email.com",
            username="baja",
            password=hash_worker,
            role=UserRole.WORKER,
        )
        print(f"\tWorker user '{worker.username}' created...")
        
        print(" - Adding users to the database...")
        db.add_all([admin, lead, worker])
        db.flush()
        
        team.team_lead_id = lead.id
        admin_team.team_lead_id = admin.id

        print(" - Uploading documents...")
        print(" - Creating document entry for Doc1...")
        doc1_file_path = os.path.join(team.team_path, "Doc1.txt")
        doc1 = Document( 
            id=str(uuid4()),
            team_id=team.id, 
            filename="Doc1.txt", 
            filetype="txt",
            filepath=doc1_file_path
        )
        print(" - Creating document entry for Doc2...")
        doc2_file_path = os.path.join(team.team_path, "Doc2.txt")
        doc2 = Document( 
            id=str(uuid4()),
            team_id=team.id, 
            filename="Doc2.txt", 
            filetype="txt",
            filepath=doc2_file_path
        )

        print(" - Adding documents to the database...")
        db.add_all([doc1, doc2])

        db.commit()
        print("\nSeeded successfully! :3\n")
