from .base_model import BaseModel


class ModelRegistry:
    def __init__(self):
        self._registry: dict[str, BaseModel] = {}

    def register(self, name: str, model_class):
        self._registry[name] = model_class

    def get(self, name: str) -> "BaseModel":
        model_class = self._registry.get(name)
        if model_class is None:
            raise ValueError(f"Model {name} not found in registry")
        return model_class()

    def items(self):
        return self._registry.items()


model_registry = ModelRegistry()
