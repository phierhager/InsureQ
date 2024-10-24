from .registry import model_registry
from .classical.logistic_regression import LogisticRegression
from .classical.random_forest import RandomForestClassifier
from .quantum.vqc import QuantumVQCModel
from .quantum.qsvm import QuantumQSVCModel

# Register models
model_registry.register("logistic_regression", LogisticRegression())
model_registry.register("random_forest", RandomForestClassifier())
model_registry.register("vqc", QuantumVQCModel())
model_registry.register("qsvm", QuantumQSVCModel())

__all__ = ["model_registry"]
