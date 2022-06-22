from __future__ import annotations

from dataclasses import field
from datetime import datetime
from enum import Enum
from typing import Type, ClassVar

import marshmallow
from marshmallow_dataclass import dataclass
from marshmallow import Schema, fields
from marshmallow_enum import EnumField


@dataclass(repr=False, eq=False)
class ModelAdapterState(Enum):
    READY = 0
    BUSY = 1

    # def __repr__(self):
    #     return "ModelAdapterState."+self.name

@dataclass(order=True)
class ModelAdapter:
    name: str
    version: str
    uri: str        # = field(metadata={"marshmallow_field": fields.Url()})
    max_workers: int
    used_workers: int
    id: str = field(default=None)
    status: ModelAdapterState = field(default=ModelAdapterState.READY)
    owner: str = field(default=None)
    last_seen: datetime = field(default=datetime.now())
    # support for Schema generation in Marshmallow
    Schema: ClassVar[Type[Schema]] = Schema

    # class Meta:
    #     ordered = True # order the fields

    def update(self, update_data: ModelAdapter):
        self.name = update_data.name
        self.version = update_data.version
        self.uri = update_data.uri
        self.max_workers = update_data.max_workers
        self.used_workers = update_data.used_workers
        self.status = update_data.status
        self.owner = update_data.owner
        self.last_seen = datetime.now()


# currently only supports searching for strings
class ModelAdapterSearchArgsSchema(marshmallow.Schema):
    name = fields.String()
    version = fields.String()
    owner = fields.String()
    uri = fields.String()
    max_workers = marshmallow.fields.Integer()
    used_workers = marshmallow.fields.Integer()
    status = EnumField(ModelAdapterState, default=ModelAdapterState.READY)

    class Meta:
        ordered = True
