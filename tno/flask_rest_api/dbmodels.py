import uuid
from dataclasses import dataclass
from enum import Enum

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy_utils import ChoiceType

from tno.flask_rest_api import db


class BaseModel(db.Model):
    """
    A base model containing an ID and created / update timestamps, with sensible defaults.
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class User(BaseModel):
    name = db.Column(db.String)


class Project(BaseModel):
    """
    A collection of measures that was taken.
    """

    name = db.Column(db.String)
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_by = db.relationship(User)
