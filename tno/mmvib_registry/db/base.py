from tno.mmvib_registry.models.modeladapter import ModelAdapter
from abc import ABC, abstractmethod


class RegistryDB(ABC):
    @abstractmethod
    def get_all(self) -> list[ModelAdapter]:
        pass

    @abstractmethod
    def add_model(self, model: ModelAdapter):
        pass

    @abstractmethod
    def update_model(self, model_id: str, update_data) -> ModelAdapter:
        pass

    @abstractmethod
    def get_by_id(self, model_id: str) -> ModelAdapter:
        pass

    @abstractmethod
    def delete(self, model_id: str):
        pass

    @abstractmethod
    def search(self, filter: dict) -> list[ModelAdapter]:
        pass


class ModelNotFoundException(Exception):
    def __init__(self, msg: str):
        self.message = msg

