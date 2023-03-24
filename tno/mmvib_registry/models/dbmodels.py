from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from tno.mmvib_registry import sa
from tno.mmvib_registry.models.modeladapter import ModelAdapter, ModelAdapterState


class ModelAdapterSQL(sa.Model):
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    version: Mapped[str]
    uri: Mapped[str]
    max_workers: Mapped[int]
    used_workers: Mapped[int]
    status: Mapped[ModelAdapterState]
    owner: Mapped[str]
    last_seen: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    @classmethod
    def from_model_adapter(cls, model_adapter: ModelAdapter) -> ModelAdapterSQL:
        return ModelAdapterSQL(
            id=model_adapter.id,
            name=model_adapter.name,
            version=model_adapter.version,
            uri=model_adapter.uri,
            max_workers=model_adapter.max_workers,
            used_workers=model_adapter.used_workers,
            status=model_adapter.status,
            owner=model_adapter.owner,
            last_seen=model_adapter.last_seen,
        )

    def to_model_adapter(self) -> ModelAdapter:
        return ModelAdapter(
            id=self.id,
            name=self.name,
            version=self.version,
            uri=self.uri,
            max_workers=self.max_workers,
            used_workers=self.used_workers,
            status=self.status,
            owner=self.owner,
            last_seen=self.last_seen,
        )

    def update_with_model_adapter(self, update_data):
        self.name = update_data.name
        self.version = update_data.version
        self.uri = update_data.uri
        self.max_workers = update_data.max_workers
        self.used_workers = update_data.used_workers
        self.status = update_data.status
        self.owner = update_data.owner
        self.last_seen = datetime.utcnow()
