from tno.mmvib_registry.db.base import ModelNotFoundException, RegistryDB
from tno.mmvib_registry.models.modeladapter import ModelAdapter


class MemoryDB(RegistryDB):
    def __init__(self):
        print("Init memory db: empty db")
        self._models: list[ModelAdapter] = []

    def get_all(self) -> list[ModelAdapter]:
        return self._models

    def add_model(self, model: ModelAdapter):
        print("Adding model")
        existing = [m for m in self._models if m.uri.lower() == model.uri.lower()]
        if len(existing) > 0:
            print(f"Removing {existing[0]}, as the URI is the same as the added one: {model}")
            model.id = existing[0].id  # keep same ID
            self._models.remove(existing[0])
        self._models.append(model)
        return model

    def update_model(self, model_id: str, update_data) -> ModelAdapter:
        item = self.get_by_id(model_id)
        item.update(update_data)
        return item

    def get_by_id(self, model_id: str) -> ModelAdapter:
        for m in self._models:
            if m.id == model_id:
                return m
        raise ModelNotFoundException("Cant find model with id=" + model_id)

    def delete(self, model_id: str):
        m: ModelAdapter = self.get_by_id(model_id)
        self._models.remove(m)

    def search(self, filter: dict) -> list[ModelAdapter]:
        result_list = []
        for m in self._models:
            is_match = True
            for k, v in filter.items():
                if hasattr(m, k):
                    value = m.__getattribute__(k)
                    if isinstance(value, str): # do some 'intelligent' matching
                        is_match = is_match and (v.lower() == value.lower())
                    else:
                        is_match = is_match and (value == v)
                if not is_match: # no match, don't look further...
                    continue
            if is_match:
                result_list.append(m)
        return result_list
