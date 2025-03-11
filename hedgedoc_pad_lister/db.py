from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

SCHEMA_VERSION = "20220901102800-convert-history-to-longtext.js"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Permission(Enum):
    freely = "freely"
    editable = "editable"
    limited = "limited"
    locked = "locked"
    protected = "protected"
    private = "private"


class Note(db.Model):
    __tablename__ = "Notes"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]]
    permission: Mapped[Permission]
    lastchangeAt: Mapped[Optional[datetime]]
    alias: Mapped[Optional[str]]
    revisions: Mapped[List["Revision"]] = relationship(back_populates="note")


class Revision(db.Model):
    __tablename__ = "Revisions"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    noteId: Mapped[UUID] = mapped_column(ForeignKey("Notes.id"))
    note: Mapped["Note"] = relationship(back_populates="revisions")


class SequelizeMeta(db.Model):
    __tablename__ = "SequelizeMeta"

    name: Mapped[str] = mapped_column(primary_key=True)
