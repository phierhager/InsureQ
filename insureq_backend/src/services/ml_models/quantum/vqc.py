from qiskit.circuit.library import TwoLocal
from qiskit_machine_learning.algorithms.classifiers import VQC
from qiskit_machine_learning.datasets import ad_hoc_data
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from qiskit_algorithms.optimizers import COBYLA
from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Sampler
from qiskit.circuit.library import ZZFeatureMap
from ..base_model import BaseModel


class QuantumVQCModel(BaseModel):
    def __init__(self, num_features=4):
        ansatz = RealAmplitudes(num_qubits=num_features, reps=3)

        optimizer = COBYLA(maxiter=100)
        sampler = Sampler()
        feature_map = ZZFeatureMap(feature_dimension=num_features, reps=1)
        # Initialize the quantum classifier (VQC) with default settings
        self.model = VQC(
            sampler=sampler, feature_map=feature_map, ansatz=ansatz, optimizer=optimizer
        )

    def train(self, X_train, y_train):
        """
        Train the quantum classifier on the training data.
        """
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test):
        """
        Evaluate the quantum model on test data and return performance metrics.
        """
        predictions = self.model.predict(X_test)

        return {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(
                y_test, predictions, average="weighted"
            ),  # Use weighted for multiclass
            "recall": recall_score(y_test, predictions, average="weighted"),
            "f1_score": f1_score(y_test, predictions, average="weighted"),
        }
