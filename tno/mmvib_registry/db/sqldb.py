from typing import Type

from tno.mmvib_registry import sa
from tno.mmvib_registry.db.base import RegistryDB
from tno.mmvib_registry.models.dbmodels import ModelAdapterSQL
from tno.mmvib_registry.models.modeladapter import ModelAdapter


class SqlDB(RegistryDB):
    def __init__(self):
        print("init db")

    def get_all(self) -> list[ModelAdapter]:
        model_adapters = sa.session.query(ModelAdapterSQL).all()
        return [model_adapter.to_model_adapter() for model_adapter in model_adapters]

    def add_model(self, model: ModelAdapter):
        model_adapter_sql = ModelAdapterSQL.from_model_adapter(model)
        existing: Type[ModelAdapterSQL] | None = sa.session.query(ModelAdapterSQL).where(ModelAdapterSQL.uri == model_adapter_sql.uri).first()
        if existing is not None:
            print(f"Updating model {model_adapter_sql.name}, as {model_adapter_sql.uri}, is already present")
            model_adapter_sql.id = existing.id  # keep same ID, but update the rest.
            sa.session.delete(existing)
        sa.session.add(model_adapter_sql)
        sa.session.commit()
        return model_adapter_sql.to_model_adapter()

    def update_model(self, model_id: str, update_data) -> ModelAdapter:
        model_adapter: ModelAdapterSQL | None = sa.session.query(ModelAdapterSQL).get(model_id)
        if model_adapter is None:
            raise ModelNotFoundException("Cant find model with id=" + model_id)
        model_adapter.update_with_model_adapter(update_data)
        sa.session.commit()
        return model_adapter.to_model_adapter()

    def get_by_id(self, model_id: str) -> ModelAdapter:
        model_adapter: ModelAdapterSQL | None = sa.session.query(ModelAdapterSQL).get(model_id)
        if model_adapter is None:
            raise ModelNotFoundException("Cant find model with id=" + model_id)
        return model_adapter.to_model_adapter()

    def delete(self, model_id: str):
        model_adapter: ModelAdapterSQL | None = sa.session.query(ModelAdapterSQL).get(model_id)
        if model_adapter is None:
            raise ModelNotFoundException("Cant find model with id=" + model_id)
        sa.session.delete(model_adapter)
        sa.session.commit()

    def search(self, filter: dict) -> list[ModelAdapter]:
        # TODO: This should work with nice SQL queries.
        models = [model.to_model_adapter() for model in sa.session.query(ModelAdapterSQL)]
        result_list = []
        for m in models:
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

