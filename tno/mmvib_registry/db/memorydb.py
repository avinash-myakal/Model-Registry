import uuid
from datetime import datetime
from enum import Enum
from typing import List

from werkzeug.exceptions import HTTPException

from tno.mmvib_registry.models.modeladapter import ModelAdapter, ModelAdapterState


class MemoryDB:
    def __init__(self):
        print("init db")
        self._models: List[ModelAdapter] = []
        dummy = ModelAdapter(name="ESSIM", version="1.0", last_seen=datetime.now(), max_workers=1, used_workers=1,
                             status=ModelAdapterState.BUSY, uri="https://essim.hesi.energy/api",
                             owner="Edwin", id="uniqueid")
        self._models.append(dummy)

    def get_all(self) -> List[ModelAdapter]:

        return self._models

    def add_model(self, model:ModelAdapter):
        print("Adding model")
        self._models.append(model)

    def get_by_id(self, model_id: str) -> ModelAdapter:
        for m in self._models:
            if m.id == model_id:
                return m
        raise ModelNotFoundException("Cant find model with id=" + model_id)

    def delete(self, model_id: str):
        m: ModelAdapter = self.get_by_id(model_id)
        self._models.remove(m)

    def search(self, filter: dict) -> List[ModelAdapter]:
        result_list = []
        for m in self._models:
            is_match = True
            for k, v in filter.items():
                if hasattr(m, k):
                    value = m.__getattribute__(k)
                    if isinstance(value, str): # do some 'intelligent' matching
                        is_match = is_match and (v.lower() in value.lower())
                    else:
                        is_match = is_match and (value == v)
                if not is_match: # no match, don't look further...
                    continue
            if is_match:
                result_list.append(m)
        return result_list


class ModelNotFoundException(Exception):
    def __init__(self, msg: str):
        self.message = msg

