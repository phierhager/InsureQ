from qiskit_machine_learning.algorithms.classifiers import QSVC
from qiskit_machine_learning.datasets import ad_hoc_data
from qiskit.circuit.library import ZZFeatureMap
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from ..base_model import BaseModel
from qiskit.primitives import Sampler
from qiskit.circuit.library import ZZFeatureMap
from qiskit.primitives import Sampler
from qiskit_algorithms.state_fidelities import ComputeUncompute
from qiskit_machine_learning.kernels import FidelityQuantumKernel


class QuantumQSVCModel(BaseModel):
    def __init__(self, num_features=4):
        adhoc_feature_map = ZZFeatureMap(
            feature_dimension=num_features, reps=2, entanglement="linear"
        )
        sampler = Sampler()
        fidelity = ComputeUncompute(sampler=sampler)
        adhoc_kernel = FidelityQuantumKernel(
            fidelity=fidelity, feature_map=adhoc_feature_map
        )

        # Initialize the quantum classifier (QSVC) with default settings
        self.model = QSVC(quantum_kernel=adhoc_kernel)

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
