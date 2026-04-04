import enum

from datetime import datetime, timezone

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .session import Base

def utc_now():
    return datetime.now(timezone.utc)

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(primary_key=True)
    team_id: Mapped[str] = mapped_column(ForeignKey("teams.id"), index=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    filetype: Mapped[str] = mapped_column(nullable=False)
    filepath: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now)

    team: Mapped["Team"] = relationship("Team", back_populates="documents")

class UserRole(enum.Enum):
    ADMIN = "Admin"
    TEAM_LEAD = "Team Lead"
    SUPERVISOR = "Supervisor"
    WORKER = "Worker"

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    team_id: Mapped[str | None] = mapped_column(
        ForeignKey("teams.id"),
        index=True,
        nullable=True,
    )
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)

    team: Mapped["Team"] = relationship(
        "Team", 
        back_populates="users",
        foreign_keys=[team_id]
    )

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[str] = mapped_column(primary_key=True)
    team_lead_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    team_name: Mapped[str] = mapped_column(nullable=False)
    team_path: Mapped[str] = mapped_column(nullable=False)

    users: Mapped[list["User"]] = relationship(
        "User", 
        back_populates="team",
        foreign_keys="User.team_id"
    )
    documents: Mapped[list["Document"]] = relationship(
        "Document", 
        back_populates="team"
    )
    team_lead: Mapped["User"] = relationship(
        "User", 
        foreign_keys=[team_lead_id]
    )
